# AgenticBuild: Development Roadmap and Architecture History

## 1. Project Evolution & History
AgenticBuild evolved from an initial prototype (practiceAI) into a sophisticated, multi-tenant AI agent platform. The core goal was to move beyond simple chat interfaces to an autonomous developer agent capable of writing, testing, and self-correcting code.

### Phase 1: Foundation (v1)
- **Initial Setup**: Built the core FastAPI backend and Streamlit frontend.
- **Authentication**: Implemented JWT-based multi-tenancy to isolate user projects.
- **Basic Generation**: Implemented simple "one-shot" code generation.

### Phase 2: Agentic Intelligence (v2-v3)
- **LangGraph Integration**: Transitioned from linear chains to a stateful graph-based architecture.
- **Self-Healing Loop**: Added a `validator_node` and `coder_node` loop that autonomously fixes syntax errors and logic gaps (up to 3 retries).
- **Feasibility Analysis**: Added an `analyzer_node` to pre-screen requests, ensuring the agent stays within its technical capabilities.
- **Project Branding**: Standardized the entire ecosystem under the **AgenticBuild** brand.

## 2. Currently Implemented Features
- [x] **Stateful Orchestration**: Complex multi-step reasoning using LangGraph.
- [x] **Autonomous Code Recovery**: Built-in retry logic for self-correcting code.
- [x] **Multi-Tenant Architecture**: Secure JWT auth with SQLite persistence for projects/chat.
- [x] **Full-Stack Scaffolding**: Support for React/Tailwind frontends and Python scripts.
- [x] **UI/UX Polish**: Scrollable chat containers, modern glassmorphic aesthetics, and live previews.
- [x] **Flexible LLM Factory**: Defaulting to `openai/gpt-oss-120b` on Groq with OpenAI fallback.

## 3. Future Roadmap (v4 and Beyond)

### Task 1: Multi-Agent Collaboration Nodes
- **Goal**: Transition from a single "Senior Engineer" agent to a specialized team.
- **Components**: 
    - `Product Manager Node`: Refines requirements and creates detailed user stories.
    - `QA Engineer Node`: Writes and executes unit tests for generated code.
    - `DevOps Node`: Handles automated deployment and environment configuration.

### Task 2: Local Code Execution & Sandboxing
- **Goal**: Safely execute and test generated code in real-time.
- **Approach**: Integrate with Docker or a WebAssembly-based sandbox to run Python/Node code during the `validator_node` phase.

### Task 3: Git Integration for Projects
- **Goal**: Allow users to track versions of their generated applications.
- **Features**: Automatically initialize a git repo in `projects/{name}/` and create commits for every iterative update requested by the user.

### Task 4: Real-time Collaborative Editing
- **Goal**: Allow users to edit generated code directly in the UI with AI assistance.
- **Approach**: Integrate a code editor (like Monaco) into the Streamlit frontend.

---
*Note: This roadmap serves as the persistent planning context for AgenticBuild.*
