# AgenticBuild Standardization & UI Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize the project under the name "AgenticBuild", implement a scrollable chat window, and overhaul the documentation.

**Architecture:** 
- Update project-level metadata (`pyproject.toml`, UI titles).
- Inject custom CSS into the Streamlit frontend to create a fixed-height, scrollable chat message container.
- Reorganize planning documents into the `docs/superpowers/plans/` structure.
- Completely rewrite the `README.md` to be product-focused.

**Tech Stack:** Python, Streamlit, FastAPI, LangGraph.

---

### Task 1: Reorganize Plans & Specs

**Files:**
- Create: `docs/superpowers/plans/.gitkeep`
- Create: `docs/superpowers/specs/.gitkeep`
- Modify: Move `plans/v2-scaffolder-plan.md` -> `docs/superpowers/plans/2026-04-26-v2-scaffolder-plan.md`

- [ ] **Step 1: Create directories**
Run: `mkdir -p docs/superpowers/plans docs/superpowers/specs`

- [ ] **Step 2: Move existing plan**
Run: `mv plans/v2-scaffolder-plan.md docs/superpowers/plans/2026-04-26-v2-scaffolder-plan.md`

- [ ] **Step 3: Remove old plans directory**
Run: `rm -rf plans`

- [ ] **Step 4: Commit**
```bash
git add docs/superpowers/
git commit -m "chore: reorganize docs and plans into standardized structure"
```

### Task 2: Standardize Branding (Backend & Config)

**Files:**
- Modify: `pyproject.toml`
- Modify: `backend/app/main.py`
- Modify: `backend/app/services/agent.py`

- [ ] **Step 1: Update pyproject.toml name**
```toml
[project]
name = "agenticbuild"
```

- [ ] **Step 2: Update FastAPI title in backend/app/main.py**
```python
app = FastAPI(title="AgenticBuild API")
```

- [ ] **Step 3: Commit**
```bash
git add pyproject.toml backend/app/main.py
git commit -m "brand: rename project to AgenticBuild in backend and config"
```

### Task 3: Implement Scrollable Chat Window & UI Branding

**Files:**
- Modify: `frontend/app.py`
- Modify: `frontend/components/chat_ui.py`
- Modify: `frontend/components/sidebar.py`

- [ ] **Step 1: Add Custom CSS for scrolling in frontend/app.py**
```python
# Add this inside the st.markdown style block
st.markdown("""
<style>
    /* Chat message container styling */
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
    }
    /* Hide scrollbar for Chrome, Safari and Opera */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)
```

- [ ] **Step 2: Wrap messages in a container in frontend/components/chat_ui.py**
```python
# Wrap the message loop in a div with the chat-container class
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "preview_url" in message and message["preview_url"]:
            st.link_button("🌐 Open Live Preview", message["preview_url"])
st.markdown('</div>', unsafe_allow_html=True)

# Also update the title
st.title("🤖 AgenticBuild Workspace")
```

- [ ] **Step 3: Update sidebar title in frontend/components/sidebar.py**
```python
st.title("⚙️ AgenticBuild Settings")
```

- [ ] **Step 4: Commit**
```bash
git add frontend/
git commit -m "feat: implement scrollable chat window and update UI branding"
```

### Task 4: Documentation Overhaul (README.md)

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite README.md**
```markdown
# AgenticBuild 🤖

AgenticBuild is a high-signal AI agent platform that builds standalone web applications and Python scripts through conversational dialogue. Powered by LangGraph and FastAPI, it features self-correcting code generation and a polished, developer-centric UI.

## 🚀 Key Functionalities
- **Instant Project Scaffolding:** Build responsive web apps with Tailwind CSS and GSAP animations.
- **Self-Correction Loop:** The agent automatically validates code and retries up to 3 times if errors are found.
- **Context-Aware Development:** The agent remembers previous instructions and project state.
- **Live Previews:** Instant viewing of generated web apps.

## ⚙️ Usage
1. Run the initialization script: `uv run python init_and_run.py`
2. Signup/Login to access your workspace.
3. Use **🏗️ Build Project** mode to start a new app.
4. Use **💬 Chat** mode for general queries or refinement.

## 🧹 Maintenance
If you need to reset your environment, use the provided cleanup tool:
```bash
uv run python clear_db.py
```
*This will wipe all users, database records, and generated project files.*

## 🛠️ Tech Stack
- **Backend:** FastAPI, SQLModel (SQLite)
- **Frontend:** Streamlit
- **AI Orchestration:** LangGraph, LangChain
- **Inference:** Groq (Llama 3)
```

- [ ] **Step 2: Commit**
```bash
git add README.md
git commit -m "docs: complete overhaul of README for AgenticBuild"
```
