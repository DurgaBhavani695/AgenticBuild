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

## 🚧 Security Roadmap (TODO)
To transition from a prototype to a production-hardened platform, the following security enhancements are prioritized:

- [ ] **Prompt Injection Mitigation**: Implement advanced system-level scaffolding to detect and block adversarial queries designed to bypass agent constraints.
- [ ] **Resource Damage Prevention**: Sandbox the agent's file-writing capabilities to prevent unauthorized modifications outside of designated project directories.
- [ ] **Input/Output Sanitization**: Add a security layer to scrub sensitive data or PII from both user prompts and AI responses before they reach the UI or database.
- [ ] **Bad Actor Detection**: Implement behavioral heuristics and rate-limiting to catch and block users attempting data theft or resource misuse.
- [ ] **Secure Error Handling**: Refactor exception logic to ensure raw tracebacks or sensitive system information are never displayed to the end-user.
- [ ] **Output Verification**: Add a final "Security Auditor" node in LangGraph to verify that generated code is safe and free of common vulnerabilities (XSS, SQLi).

---

## ✨ Future Roadmap (TODO)
- [ ] **UI Stabilization**: Implement comprehensive UI fixes to tighten up bugs, improve consistency, and enhance the Glassmorphism experience.

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
