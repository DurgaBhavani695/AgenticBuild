# GEMINI.md - Project Context

This file provides instructional context for Gemini CLI interactions within the `AgenticBuild` project.

## Project Overview

**Project Name:** AgenticBuild
**Type:** Agentic AI SaaS (v3)
**Primary Technology:** Python (>= 3.14), FastAPI, SQLModel (SQLite), Streamlit, LangChain, LangGraph, Groq.

The project is structured as a multi-tenant AI agent platform. v3 features user authentication (JWT), persistent project/chat history (SQLite), a modular frontend architecture, and incremental project updates.

## Architecture

- **Backend (`backend/app/`):** FastAPI application.
    - `core/`: Configuration, security, and authentication utilities.
    - `api/`: REST endpoints (Auth, Projects, Chat).
    - `services/`: AI logic including `llm_factory` and `langgraph` agents.
    - `models/`: Database models (User, Project, Session) and Pydantic schemas.
- **Frontend (`frontend/`):** Modular Streamlit application.
    - `components/`: UI pieces (Auth, Sidebar, Chat).
    - `services/`: API client and state management.
    - `app.py`: Main orchestrator.

## Building and Running

### Fast Setup (Recommended)
The project includes a one-click initialization and run script:
```bash
uv run python init_and_run.py
```
This script handles dependency syncing, `.env` configuration, and launches both servers concurrently.

### Environment Setup
1. Create a `.env` file from `.env.example`.
2. Add your `GROQ_API_KEY`.
3. Install dependencies:
   ```bash
   uv sync
   ```

### Manual Execution
To run the full stack manually, you need two terminals:

**Terminal 1 (Backend):**
```bash
uv run uvicorn backend.app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
uv run streamlit run frontend/app.py
```

## Development Conventions

- **TDD:** Always write unit tests in `tests/` before implementing new backend features. Use `pytest`.
- **Generalization:** Use the `llm_factory` to instantiate chat models.
- **Auth:** All project and chat endpoints require JWT authentication.
- **State Management:** Use LangGraph `StateGraph` for AI workflows.

## TODOs
- [ ] v4: Implement multi-agent collaboration nodes.
- [ ] v4: Add local code execution in Docker for better safety.
- [ ] v4: Add Git integration to track changes in generated projects.
