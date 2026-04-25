# practiceAI 🤖

An agentic AI platform built with FastAPI, Streamlit, and LangGraph.

## 🚀 Overview
practiceAI is a modular AI agent project designed to scale from simple chat interactions to complex, multi-step agentic workflows. 

- **v1 (Current):** A generalized chat interface using LangGraph to orchestrate LLM calls (via Groq).
- **v2 (Roadmap):** AI-driven code generation and local execution with feedback loops.

## 🛠️ Tech Stack
- **Language:** Python 3.14+
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **AI Orchestration:** LangGraph & LangChain
- **Inference:** Groq (Llama 3, Mixtral, etc.)
- **Dependency Management:** `uv`

## 📦 Project Structure
```text
practiceAI/
├── backend/app/
│   ├── api/          # FastAPI Routes
│   ├── core/         # Configuration (Pydantic Settings)
│   ├── models/       # Data Schemas
│   └── services/     # AI Logic (LLM Factory & LangGraph)
├── frontend/         # Streamlit Chat UI
└── pyproject.toml    # Project Dependencies
```

## ⚙️ Setup & Installation

### 1. Prerequisites
Ensure you have `uv` installed. If not, install it via:
```powershell
pip install uv
```

### 2. Environment Configuration
Copy the example environment file and add your [Groq API Key](https://console.groq.com/keys).
```powershell
cp .env.example .env
```

### 3. Install Dependencies
```powershell
uv sync
```

## 🏃 Running the Application

You will need two terminals to run the full stack:

### Terminal 1: Backend (FastAPI)
```powershell
uv run uvicorn backend.app.main:app --reload
```
The API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Terminal 2: Frontend (Streamlit)
```powershell
uv run streamlit run frontend/app.py
```
The chat interface will be available at [http://localhost:8501](http://localhost:8501).

## 🔧 Customization
You can easily swap LLM providers or models by updating the `.env` file:
```text
LLM_PROVIDER=groq
GROQ_MODEL_NAME=llama3-70b-8192
```

## 🛣️ Roadmap
- [x] v1: Basic LangGraph chat integration.
- [ ] v2: Implement a code-executor node in the graph.
- [ ] v2: Add automated testing for generated code.
- [ ] v2: Support for local LLMs via Ollama.
