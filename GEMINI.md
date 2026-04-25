# GEMINI.md - Project Context

This file provides instructional context for Gemini CLI interactions within the `practiceAI` project.

## Project Overview

**Project Name:** practiceAI
**Type:** Agentic AI Project (v1)
**Primary Technology:** Python (>= 3.14), FastAPI, Streamlit, LangChain, LangGraph, Groq.

The project is structured as a generalized AI agent platform. v1 features a chat interface that routes messages through a FastAPI backend to a LangGraph-orchestrated LLM (Groq).

## Architecture

- **Backend (`backend/app/`):** FastAPI application.
    - `core/`: Configuration and environment settings.
    - `api/`: REST endpoints (e.g., `/api/chat`).
    - `services/`: AI logic including `llm_factory` and `langgraph` agents.
    - `models/`: Pydantic schemas for API requests/responses.
- **Frontend (`frontend/`):** Streamlit chat interface.

## Building and Running

### Environment Setup
The project uses `uv` for dependency management.
1. Create a `.env` file from `.env.example` and add your `GROQ_API_KEY`.
2. Install dependencies:
   ```bash
   uv sync
   ```

### Execution
To run the full stack, you need two terminals:

**Terminal 1 (Backend):**
```bash
uv run uvicorn backend.app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
uv run streamlit run frontend/app.py
```

## Development Conventions

- **Generalization:** Always use the `llm_factory` to instantiate chat models to ensure easy swapping of providers.
- **State Management:** Use LangGraph `StateGraph` for all AI workflows to maintain scalability for v2.
- **Typing:** Use Pydantic models for all API interactions.

## TODOs
- [ ] v2: Implement AI workflow for code generation and execution.
- [ ] Add more LLM providers to `llm_factory.py`.
- [ ] Add unit tests for the LangGraph workflow.
