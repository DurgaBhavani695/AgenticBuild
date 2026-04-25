# AgenticBuild 🤖
**Autonomous Full-Stack AI Engineer**

AgenticBuild is an AI-native SaaS platform that transforms natural language into production-ready web applications. Unlike traditional "one-shot" generators, it uses **Agentic Loops** to architect, implement, and self-correct code until it works.

---

## ✨ Key Features
- **Self-Healing Code Engine**: Implements a recursive "Test-and-Repair" loop. If the generated code has bugs, the agent detects, analyzes, and fixes them autonomously before delivery.
- **LangGraph Orchestration**: Uses stateful directed acyclic graphs (DAGs) to manage complex multi-step reasoning, ensuring high architectural consistency.
- **Multi-Tenant Security**: Enterprise-ready architecture with JWT authentication and isolated user workspaces.
- **High-Fidelity Scaffolding**: Generates immersive single-page applications (Tailwind/Three.js/GSAP) and Python scripts with live previews in seconds.

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
