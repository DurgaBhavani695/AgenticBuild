# AgenticBuild 🤖
**Autonomous Full-Stack AI Engineer**

AgenticBuild is an AI-native SaaS platform that transforms natural language into production-ready web applications. Unlike traditional "one-shot" generators, it uses **Agentic Loops** to architect, implement, and self-correct code until it works.

---

## ✨ Key Features
- **Self-Healing Code Engine**: Implements a recursive "Test-and-Repair" loop. If the generated code has bugs, the agent detects, analyzes, and fixes them autonomously before delivery.
- **LangGraph Orchestration**: Uses stateful directed acyclic graphs (DAGs) to manage complex multi-step reasoning, ensuring high architectural consistency.
- **Incremental Project Updates**: Unlike one-shot generators, AgenticBuild understands your existing codebase. You can request updates, add features, or refactor existing projects through conversational dialogue.
- **Hybrid Support**: Seamlessly switch between **Chat Mode** (for general architectural advice and queries) and **Project Mode** (for autonomous building).

---

## 🧠 Smart Session & Context Management
- **Multi-Session Architecture**: Create and manage multiple concurrent workstreams. Switch between different feature builds without losing progress.
- **Session-Driven Context**: Each project maintains a dedicated chat history and state. The agent remembers previous decisions, requested styles, and technical constraints specific to that session.
- **Enterprise Multi-Tenancy**: Built-in JWT authentication ensures that sessions and projects are strictly isolated between users.
- **Persistent Project History**: All generated code and conversation logs are stored locally (SQLite), allowing you to resume any build exactly where you left off.

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
Create a `.env` file (see `.env.example`):
```env
GROQ_API_KEY=your_key_here
```

### 3. Launch AgenticBuild
```bash
uv run python init_and_run.py
```

---

## 🛠️ Individual Component Execution
If you prefer to run the services separately:

### **Backend (FastAPI)**
```bash
uv run uvicorn backend.app.main:app --reload
```

### **Frontend (Streamlit)**
```bash
uv run streamlit run frontend/app.py
```

---

## 🏗️ Technical Stack
- **Backend**: Python 3.14, FastAPI, SQLModel (SQLite), JWT
- **AI Brain**: LangGraph, LangChain, Groq (openai/gpt-oss-120b)
- **Frontend**: Streamlit, LocalStorage API
- **Deployment**: Local live-mounting for instant previews
