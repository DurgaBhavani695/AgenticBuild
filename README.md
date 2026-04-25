# AgenticBuild 🤖
**Autonomous Full-Stack AI Engineer**

AgenticBuild is an AI-native platform that transforms natural language into production-ready web applications. Unlike traditional "one-shot" generators, it uses **Agentic Loops** powered by LangGraph to architect, implement, and self-correct code until it works.

---

## ✨ Key Features

### 🧠 Intelligent Orchestration
- **Self-Healing Code Engine**: Implements a recursive "Test-and-Repair" loop. If the generated code has bugs or formatting issues, the agent detects, analyzes, and fixes them autonomously across multiple retries.
- **LangGraph State Management**: Uses stateful directed acyclic graphs (DAGs) to manage complex multi-step reasoning, ensuring high architectural consistency.
- **Smart Fallback Mechanism**: Automatically pivots from complex multi-file architectures to robust single-file applications if technical constraints (like token limits) are hit.
- **Feasibility Analysis**: Pre-screens every request to ensure it stays within system capabilities, providing **💡 Suggested Alternatives** for non-feasible tasks.

---

## 🖼️ Visual Gallery
*Examples of the AgenticBuild workspace and high-fidelity applications generated autonomously.*

<div align="center">
  <img src="docs/assets/screenshots/screenshot-1.jpeg" width="45%" alt="AgenticBuild Dashboard"/>
  <img src="docs/assets/screenshots/screenshot-2.jpeg" width="45%" alt="AI Reasoning Process"/>
</div>
<div align="center">
  <img src="docs/assets/screenshots/screenshot-3.jpeg" width="45%" alt="Generated Weather App - Overview"/>
  <img src="docs/assets/screenshots/screenshot-4.jpeg" width="45%" alt="Generated Weather App - Detail"/>
</div>
<div align="center">
  <img src="docs/assets/screenshots/screenshot-5.jpeg" width="45%" alt="Mobile Responsive View"/>
  <img src="docs/assets/screenshots/screenshot-6.jpeg" width="45%" alt="Complex 3D Logic Generation"/>
</div>
<div align="center">
  <img src="docs/assets/screenshots/screenshot-7.jpeg" width="91%" alt="Final Product Showcase"/>
</div>

---

### 🛠️ Advanced Project Management
- **Incremental Updates**: Unlike one-shot generators, AgenticBuild understands your existing codebase. You can request updates, add features, or refactor existing projects through conversational dialogue.
- **Multi-Session Workstreams**: Create and manage multiple concurrent project builds. Switch between different feature branches without losing progress.
- **Dynamic Model Switching**: Hot-swap between different "AI brains" (OpenAI 120B, Llama 4 Scout, Llama 3.3, etc.) at runtime to balance speed, cost, and reasoning power.
- **Native ZIP Exports**: Download your completed projects as ready-to-deploy archives directly from the sidebar.

### 🛡️ Enterprise-Ready Core
- **Multi-Tenant Security**: Built-in JWT authentication ensures that sessions, projects, and history are strictly isolated between users.
- **Context Pruning**: High-efficiency history management and character capping allow the agent to handle large projects without hitting server request size limits.
- **Glassmorphism UI**: A high-end, modern dashboard with blur effects, responsive layouts, and real-time build status tracking.

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install uv (modern package manager)
pip install uv

# Sync dependencies
uv sync
```

### 2. Configure Credentials
Create a `.env` file from `.env.example`:
```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
GROQ_MODEL_NAME=openai/gpt-oss-120b
```

### 3. Launch AgenticBuild
```bash
uv run python init_and_run.py
```

---

## 🚧 Security & Robustness Roadmap (TODO)
To transition from a prototype to a production-hardened platform, the following "Security-First" enhancements are prioritized. This focus ensures the platform is resilient against adversarial AI usage and protects core infrastructure:

- [ ] **Advanced Prompt Injection Mitigation**: Implement multi-layered system scaffolding and log-analysis to detect and block indirect and direct injection attacks (Jailbreaking/Adversarial prompts).
- [ ] **Filesystem Sandboxing & RBAC**: Implement strict **Role-Based Access Control (RBAC)** and containerized sandboxing for the agent's file-writing capabilities to prevent unauthorized resource access or permission escalation.
- [ ] **Data Exfiltration Prevention**: Add an egress filtering layer to sanitize AI responses, ensuring sensitive system data, PII, or internal logic is never leaked through generated code or summaries.
- [ ] **Resource Abuse Heuristics**: Implement behavioral monitoring to detect bad actors attempting to use the agent for unintended purposes (e.g., data theft, botnet construction, or unauthorized scraping).
- [ ] **Production-Grade Error Masking**: Refactor the global exception handler to provide high-level user guidance while completely masking raw system tracebacks and environment-specific metadata.
- [ ] **Automated Security Auditing**: Integrate a final "Security Auditor" node in the LangGraph workflow to perform static analysis on all generated code before it is presented to the user.

---

## ✨ Future Roadmap (TODO)
- [ ] **UI Stabilization**: Implement comprehensive UI fixes to tighten up bugs, improve consistency, and enhance the Glassmorphism experience.

---

## 🛠️ Development Methodology
AgenticBuild was developed adopting the new era of **AI-First Engineering**, leveraging autonomous agent orchestration to build an autonomous agent platform.

- **Gemini CLI & Superpowers MCP**: This project was architected and stabilized using the Gemini CLI, utilizing the **Superpowers MCP** for deep codebase research and tool integration.
- **Plan & Action Workflow**: The development followed a strict **Research -> Strategy (Plan Mode) -> Execution (Action Mode)** cycle. This ensured that complex refactors and new features were designed responsibly before a single line of code was modified.
- **Human-AI Synergy**: While AI handled the heavy lifting of implementation and debugging, it required a **deep technical understanding** to direct the agents correctly, verify their output responsibly, and manage the architectural integrity of the system.
- **The Modern Era**: This project serves as a testament to the transition from manual coding to **Agentic Orchestration**—a workflow that demands higher-level system design skills and a focus on responsible, secure AI usage.

---

## 🏗️ Technical Stack
- **Backend**: Python 3.14, FastAPI, SQLModel (SQLite), JWT
- **AI Engine**: LangGraph, LangChain, Groq (OpenAI 120B / Llama 4 / Llama 3.3)
- **Frontend**: Streamlit, LocalStorage API, GSAP, Tailwind CSS
- **Capabilities**: High-fidelity Single-Page Apps (Three.js/GSAP) and Standalone Scripts

---

## 🧹 Individual Execution
If you prefer to run the services separately:

- **Backend**: `uv run uvicorn backend.app.main:app --reload`
- **Frontend**: `uv run streamlit run frontend/app.py`
