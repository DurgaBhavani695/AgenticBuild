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
