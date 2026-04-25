# Design Spec: AgenticBuild Standardization & UI Polish

## 1. Objective
Transform the project into a professional, standalone product named **AgenticBuild**. This involves complete branding standardization, UI refinement (scrollable chat), and a cleaner project structure.

## 2. Branding & Documentation (AgenticBuild)
- **Name:** Standardize all user-facing and internal references to "AgenticBuild".
- **README.md Overhaul:**
    - Remove tool-specific metadata (Gemini/MCP mentions as primary features).
    - Focus on core value: Building apps through agentic dialogue.
    - Include clear sections for:
        - **Overview:** The "AgenticBuild" mission.
        - **Usage:** How to create, update, and manage projects.
        - **Maintenance:** Explicit documentation for `clear_db.py`.
        - **Tech Stack:** FastAPI, LangGraph, Streamlit.

## 3. UI Enhancements: Scrollable Chat
- **Problem:** Long conversations grow the page indefinitely, making the chat input hard to access.
- **Solution:** 
    - Use custom CSS to create a fixed-height scrollable container for chat messages.
    - Container will have a `max-height` (e.g., 70-80vh) and `overflow-y: auto`.
    - Ensure the scrollbar is styled to match the modern dark theme.

## 4. Folder Reorganization
- **Standardization:** Move planning documents to a unified structure.
- **New Path:** `docs/superpowers/plans/` (for `.md` plans).
- **Existing Plans:** Move `plans/v2-scaffolder-plan.md` to the new location.

## 5. Success Criteria
- [ ] Local repo name is `AgenticBuild`.
- [ ] `pyproject.toml` reflects the new project name.
- [ ] UI displays "AgenticBuild" consistently.
- [ ] Chat window remains within a fixed viewport and scrolls when content exceeds that height.
- [ ] `README.md` is clean, descriptive, and free of internal meta-context.
