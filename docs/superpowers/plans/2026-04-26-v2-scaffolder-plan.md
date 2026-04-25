# Implementation Plan: V2 Project Scaffolder

## Objective
Evolve AgenticBuild into a robust project scaffolder. The system will generate multi-file projects (React/Tailwind frontends and FastAPI backends), save them to a local workspace, and allow users to manage their project history via the Streamlit UI.

## Key Features
*   **React + Tailwind Support:** Generate modern, component-based frontends.
*   **Project Workspace:** Automatically save generated code into `projects/{project_name}/`.
*   **History & Management:** View and download previously generated projects via a Streamlit sidebar.
*   **Validation Loop:** LangGraph will verify syntax before finalizing the project.

## Implementation Steps

### 1. Backend: State & Logic
*   **`backend/app/services/agent.py`:** Update `AgentState` to include `project_name`, `files` (dict), and `project_type`.
*   **New Nodes:**
    *   `architect_node`: Plans the file structure.
    *   `coder_node`: Generates code for all planned files.
    *   `writer_node`: Saves files to the local disk.
*   **`backend/app/api/routes.py`:** Add endpoints to list projects and download them as ZIPs.

### 2. Frontend: Workspace UI
*   **`frontend/app.py`:** 
    *   Add a sidebar to list projects from the `projects/` directory.
    *   Display the generated project name and a file tree in the chat.
    *   Add a "Download .zip" button for completed projects.

### 3. Configuration
*   Update `pyproject.toml` if any new utilities (like `shutil` for zipping) are needed.
