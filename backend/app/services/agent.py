import os
import json
import operator
import re
from typing import TypedDict, Annotated, List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from .llm_factory import get_llm

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    mode: str  # 'chat' or 'project'
    project_name: str
    files: Dict[str, str]  # New/modified files (path -> content)
    existing_files: Dict[str, str]  # Currently on disk (path -> content)
    project_type: str  # e.g., 'web', 'python'
    status: str
    summary: str  # User-facing summary of changes
    is_feasible: bool
    feasibility_reason: str
    retry_count: int
    validation_error: str

def parse_json_safely(text: str):
    """Robustly extract and parse JSON from LLM response."""
    if not text:
        return None
        
    # 1. Try to find JSON block
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        # 2. Find the first '{' and last '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end+1]
    
    text = text.strip()
    
    try:
        data = json.loads(text)
        # Deep unescape for strings that might be double-escaped
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    try:
                        # If it looks like a stringified JSON string, unescape it
                        if v.startswith('"') and v.endswith('"'):
                            data[k] = json.loads(v)
                        # Handle literal \n text
                        data[k] = data[k].replace("\\n", "\n").replace('\\"', '"')
                    except:
                        pass
        return data
    except Exception:
        # 3. Handle common syntax errors (trailing commas, etc.)
        text = re.sub(r",\s*}", "}", text)
        text = re.sub(r",\s*\]", "]", text)
        try:
            return json.loads(text)
        except:
            return None

def analyzer_node(state: AgentState):
    """Assess if the project request is feasible given system constraints."""
    llm = get_llm()
    last_msg = ""
    for m in reversed(state["messages"]):
        if isinstance(m, HumanMessage):
            last_msg = m.content
            break
            
    prompt = ChatPromptTemplate.from_template(
        "You are an expert Project Feasibility Analyzer and Senior Technical Lead.\n"
        "A user wants to build: '{description}'.\n\n"
        "System Constraints:\n"
        "- Can generate single-page HTML/JS/CSS websites (utilizing Tailwind CSS, GSAP for animations, and Three.js for 3D/Canvas visuals).\n"
        "- Can generate simple standalone Python scripts.\n"
        "- CANNOT generate multi-file backend systems, mobile apps, or complex 3D games.\n\n"
        "Respond STRICTLY in JSON:\n"
        "{{\n"
        "  \"is_feasible\": true/false,\n"
        "  \"reason\": \"Brief technical explanation\"\n"
        "}}"
    )
    chain = prompt | llm
    response = chain.invoke({"description": last_msg})
    
    data = parse_json_safely(response.content)
    if data:
        return {
            "is_feasible": data.get("is_feasible", True),
            "feasibility_reason": data.get("reason", ""),
            "status": "Feasibility check complete."
        }
    
    return {
        "is_feasible": True,
        "status": "Feasibility check skipped due to parsing error."
    }

def route_after_analyzer(state: AgentState):
    if state.get("is_feasible") is False:
        return "chat"
    return "namer"

def chat_node(state: AgentState):
    if state.get("is_feasible") is False:
        reason = state.get("feasibility_reason", "This project is not feasible with current constraints.")
        return {
            "messages": [AIMessage(content=f"### ❌ Project Not Feasible\n\n{reason}")],
            "status": "Feasibility rejection returned."
        }

    # If we reached chat_node but there's a validation error, it means retries were exhausted
    validation_error = state.get("validation_error")
    
    llm = get_llm()
    context = ""
    if state.get("existing_files"):
        context = "\n\nContext - Existing Project Files:\n" + "\n".join([f"--- {p} ---\n{c[:500]}..." for p, c in state["existing_files"].items()])
    
    messages = state["messages"]
    
    # If there's an error, inform the LLM so it can explain it structured as Overview, Context, and Steps
    if validation_error:
        error_msg = HumanMessage(content=(
            f"System: The attempt to generate code for this project failed after multiple retries. Last error: {validation_error}.\n"
            "Please explain the failure to the user and PROVIDE A SIMPLER PROMPT they can use to achieve a similar result.\n\n"
            "Structure your response as follows:\n"
            "### ❌ Build Halted\n[Brief summary of the failure]\n\n"
            "### Context\n[Acknowledgment of what was being attempted]\n\n"
            "### Steps Taken & Blockers\n- [Bullet points of blockers]\n\n"
            "### 💡 Suggested Fix\n"
            "Try this simplified prompt instead:\n"
            "> [A specific, simplified version of the user's original prompt that is more likely to succeed]"
        ))
        messages = messages + [error_msg]
    elif context:
        system_msg = HumanMessage(content=f"System: You are assisting with an existing project. Here is a summary of the current files for context (truncated if long):{context}")
        messages = [system_msg] + messages

    response = llm.invoke(messages)
    return {
        "messages": [response],
        "status": "Chat response generated."
    }

def namer_node(state: AgentState):
    if state.get("project_name"):
        return {"status": f"Using existing project: {state['project_name']}"}

    llm = get_llm()
    last_msg = ""
    for m in reversed(state["messages"]):
        if isinstance(m, HumanMessage):
            last_msg = m.content
            break
            
    prompt = ChatPromptTemplate.from_template(
        "Generate a creative, short (1-2 words), slug-friendly project name based on this description: {description}. "
        "Respond with ONLY the project name, no punctuation or extra text."
    )
    chain = prompt | llm
    response = chain.invoke({"description": last_msg})
    project_name = response.content.strip().lower().replace(" ", "-").replace("\"", "").replace("'", "")
    if not project_name:
        project_name = "awesome-project"
    return {
        "project_name": project_name,
        "status": f"Project named: {project_name}"
    }

def architect_node(state: AgentState):
    llm = get_llm()
    last_msg = ""
    for m in reversed(state["messages"]):
        if isinstance(m, HumanMessage):
            last_msg = m.content
            break
            
    project_name = state["project_name"]
    existing_files_list = list(state.get("existing_files", {}).keys())
    
    context_str = ""
    if existing_files_list:
        context_str = f"\nThis is an UPDATE to an existing project. Existing files: {existing_files_list}"

    prompt = ChatPromptTemplate.from_template(
        "You are an elite Senior Software Architect and Technical Design Authority. Based on the project name '{project_name}' and user request: '{description}', "
        "determine the most efficient and impactful architecture.\n\n"
        "GUIDELINES:\n"
        "- Use 'web' for interactive UI, dashboards, or visual applications.\n"
        "- Only include 'three.js' in the file list if the user explicitly requests 3D/immersive elements or if it adds undeniable visual impact that GSAP/Tailwind cannot achieve.\n"
        "- For COMPLEX visual requests, PREFER splitting into multiple files (index.html, styles.css, script.js) to manage token limits and maintain clean code.\n"
        "- Use 'python' for data processing, automation scripts, or CLI utilities.\n"
        "{context_str}\n\n"
        "Respond STRICTLY in JSON format:\n"
        "{{\n"
        "  \"project_type\": \"web\" or \"python\",\n"
        "  \"files\": [\"list\", \"of\", \"required\", \"files\"]\n"
        "}}"
    )
    chain = prompt | llm
    response = chain.invoke({"project_name": project_name, "description": last_msg, "context_str": context_str})
    
    data = parse_json_safely(response.content)
    if data and data.get("files"):
        return {
            "project_type": data.get("project_type", "python"),
            "files": {path: "" for path in data.get("files", [])},
            "status": f"Architected {data.get('project_type')} project."
        }
    
    return {
        "project_type": "web",
        "files": {"index.html": ""},
        "status": "Architecting fallback used."
    }

def coder_node(state: AgentState):
    llm = get_llm()
    last_msg = ""
    for m in reversed(state["messages"]):
        if isinstance(m, HumanMessage):
            last_msg = m.content
            break
    
    project_name = state["project_name"]
    project_type = state["project_type"]
    file_paths_to_gen = list(state["files"].keys())
    existing_files = state.get("existing_files", {})
    validation_error = state.get("validation_error", "")
    
    existing_context = ""
    if existing_files:
        existing_context = "\n\nEXISTING CODE (Modify these if requested or use as reference):\n"
        for path, content in existing_files.items():
            existing_context += f"--- {path} ---\n{content}\n"

    error_context = ""
    if validation_error:
        error_context = f"\n\nCRITICAL: Your previous attempt failed validation with this error: {validation_error}. PLEASE FIX THIS."

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an elite Senior Full-Stack Engineer and Creative Director. You build production-grade, high-impact web applications.\n"
            "TECHNICAL PRINCIPLES:\n"
            "- TOKEN EFFICIENCY: Write concise, high-impact code. Minimize boilerplate. Use standard CSS/Tailwind for effects whenever possible.\n"
            "- PERFORMANCE FIRST: Prefer GSAP and Tailwind animations. ONLY use Three.js if the request requires true 3D depth or immersive canvas visuals that provide undeniable value.\n"
            "- STRICT JSON: You respond ONLY with a valid JSON object. Meticulously escape quotes and newlines. Never include markdown code blocks inside JSON values."
        )),
        ("human", 
            "GOAL: Generate a professional, high-performance, and visually stunning single-page website.\n\n"
            "### UI/UX REQUIREMENTS:\n"
            "- Modern, high-end aesthetic (clean glassmorphism, depth, or minimalist dark/light themes).\n"
            "- Use Tailwind CSS (via CDN) for all styling and utility classes.\n"
            "- Generous whitespace/padding and responsive layouts.\n"
            "- Use polished typography (Inter, Poppins, etc. via Google Fonts).\n"
            "- Smooth GSAP animations for entrance and interaction effects.\n"
            "- For true 3D visualizations, utilize Three.js (via CDN) ONLY if it adds significant value.\n"
            "- Ensure the UI fits perfectly within a standard browser viewport.\n\n"
            "### DATA & API REQUIREMENTS:\n"
            "- Use ONLY free, public APIs that do NOT require authentication (e.g., Open-Meteo, REST Countries).\n"
            "- Simulate data with realistic delays if no public API exists.\n\n"
            "### PROJECT CONTEXT:\n"
            "Project: {project_name}\n"
            "Request: {description}\n"
            "{existing_context}{error_context}\n\n"
            "### OUTPUT FORMAT (CRITICAL):\n"
            "Respond ONLY with a valid JSON object containing the relative file paths and their content.\n"
            "One key MUST be 'summary' containing a structured technical breakdown (Overview, Context, Steps Taken).\n\n"
            "Generate content for: {file_paths_to_gen}"
        )
    ])
    chain = prompt | llm
    response = chain.invoke({
        "file_paths_to_gen": ", ".join(file_paths_to_gen),
        "project_name": project_name,
        "project_type": project_type,
        "description": last_msg,
        "existing_context": existing_context,
        "error_context": error_context
    })
    
    data = parse_json_safely(response.content)
    if data:
        summary = data.pop("summary", "Created/Modified files.")
        files_only = {k: v for k, v in data.items() if isinstance(v, str) and k.endswith(('.html', '.js', '.css', '.py', '.txt'))}
        
        return {
            "files": files_only,
            "status": "Coding complete.",
            "summary": summary,
            "validation_error": "" if files_only else "No valid files found in JSON response."
        }
    
    return {
        "status": "Coding failed: Malformed JSON or empty response from AI.",
        "validation_error": "Malformed JSON or empty response from AI."
    }

def validator_node(state: AgentState):
    """Validate that the required files were generated and are not empty."""
    files = state.get("files", {})
    retry_count = state.get("retry_count", 0)
    
    # If coder_node already reported an error (like malformed JSON), keep it and increment retry
    if state.get("validation_error"):
        return {"retry_count": retry_count + 1}
        
    if not files:
        return {
            "retry_count": retry_count + 1,
            "validation_error": "No files were generated."
        }
    
    # Check if all architected files have content
    for path, content in files.items():
        if not content or len(content.strip()) < 20:
            return {
                "retry_count": retry_count + 1,
                "validation_error": f"File '{path}' is too short or empty."
            }
            
    return {"validation_error": ""}

def route_after_validator(state: AgentState):
    if state.get("validation_error"):
        if state.get("retry_count", 0) < 5:
            return "coder"
        return "chat"
    return "writer"

def writer_node(state: AgentState):
    project_name = state["project_name"]
    files = state["files"]
    base_dir = os.path.join("projects", project_name)
    
    os.makedirs(base_dir, exist_ok=True)
    
    written_files = []
    for path, content in files.items():
        if not content: continue
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        written_files.append(path)
        
    summary = state.get("summary", "Created/Updated project files.")
    return {
        "messages": [AIMessage(content=summary)],
        "status": f"Done: {len(written_files)} files written."
    }

def route_by_mode(state: AgentState):
    if state.get("mode") == "project":
        return "namer"
    return "chat"

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("chat", chat_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("namer", namer_node)
workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("validator", validator_node)
workflow.add_node("writer", writer_node)

workflow.add_conditional_edges(
    START,
    route_by_mode,
    {
        "namer": "analyzer",
        "chat": "chat"
    }
)

workflow.add_conditional_edges(
    "analyzer",
    route_after_analyzer,
    {
        "namer": "namer",
        "chat": "chat"
    }
)

workflow.add_conditional_edges(
    "validator",
    route_after_validator,
    {
        "coder": "coder",
        "writer": "writer",
        "chat": "chat"
    }
)

workflow.add_edge("chat", END)
workflow.add_edge("namer", "architect")
workflow.add_edge("architect", "coder")
workflow.add_edge("coder", "validator")
workflow.add_edge("writer", END)

agent_app = workflow.compile()
