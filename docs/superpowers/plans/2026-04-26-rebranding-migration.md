# Rebranding Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand the project from "practiceAI" to "AgenticBuild" across specific files for consistent branding.

**Architecture:** Surgical text replacement in configuration and UI files.

**Tech Stack:** Python, Streamlit, Markdown.

---

### Task 1: Update init_and_run.py

**Files:**
- Modify: `init_and_run.py`

- [ ] **Step 1: Replace "PracticeAI" with "AgenticBuild" in console logs**

```python
<<<<
    print("--- Starting PracticeAI ---")
====
    print("--- Starting AgenticBuild ---")
>>>>
```

```python
<<<<
    def signal_handler(sig, frame):
        print("\nStopping PracticeAI...")
====
    def signal_handler(sig, frame):
        print("\nStopping AgenticBuild...")
>>>>
```

- [ ] **Step 2: Commit changes**

```bash
git add init_and_run.py
git commit -m "chore: update init_and_run.py branding"
```

### Task 2: Update GEMINI.md

**Files:**
- Modify: `GEMINI.md`

- [ ] **Step 1: Update project name and instructional context**

```markdown
<<<<
# GEMINI.md - Project Context

This file provides instructional context for Gemini CLI interactions within the `practiceAI` project.

## Project Overview

**Project Name:** practiceAI
====
# GEMINI.md - Project Context

This file provides instructional context for Gemini CLI interactions within the `AgenticBuild` project.

## Project Overview

**Project Name:** AgenticBuild
>>>>
```

- [ ] **Step 2: Commit changes**

```bash
git add GEMINI.md
git commit -m "chore: update GEMINI.md branding"
```

### Task 3: Update frontend/app.py

**Files:**
- Modify: `frontend/app.py`

- [ ] **Step 1: Update page_title and local storage keys**

```python
<<<<
st.set_page_config(page_title="PracticeAI", layout="wide", page_icon="🤖")

# Initialize LocalStorage
local_storage = LocalStorage()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "token" not in st.session_state:
    # Check local storage for existing token on startup
    saved_token = local_storage.getItem("practiceai_token")
    st.session_state.token = saved_token
====
st.set_page_config(page_title="AgenticBuild", layout="wide", page_icon="🤖")

# Initialize LocalStorage
local_storage = LocalStorage()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "token" not in st.session_state:
    # Check local storage for existing token on startup
    saved_token = local_storage.getItem("agenticbuild_token")
    st.session_state.token = saved_token
>>>>
```

```python
<<<<
def main():
    api_client = APIClient()
    
    # Sync token from session_state to local_storage if it was just set (e.g. after login)
    if st.session_state.token:
        local_storage.setItem("practiceai_token", st.session_state.token)
====
def main():
    api_client = APIClient()
    
    # Sync token from session_state to local_storage if it was just set (e.g. after login)
    if st.session_state.token:
        local_storage.setItem("agenticbuild_token", st.session_state.token)
>>>>
```

- [ ] **Step 2: Commit changes**

```bash
git add frontend/app.py
git commit -m "chore: update frontend/app.py branding"
```

### Task 4: Update frontend/components/auth_ui.py

**Files:**
- Modify: `frontend/components/auth_ui.py`

- [ ] **Step 1: Update title from "PracticeAI Auth" to "AgenticBuild Auth"**

```python
<<<<
def render_auth_page():
    st.title("🔐 PracticeAI Auth")
====
def render_auth_page():
    st.title("🔐 AgenticBuild Auth")
>>>>
```

- [ ] **Step 2: Commit changes**

```bash
git add frontend/components/auth_ui.py
git commit -m "chore: update frontend/components/auth_ui.py branding"
```

### Task 5: Update frontend/components/sidebar.py

**Files:**
- Modify: `frontend/components/sidebar.py`

- [ ] **Step 1: Update local storage removal key**

```python
<<<<
        if st.button("🚪 Logout", use_container_width=True):
            from streamlit_local_storage import LocalStorage
            ls = LocalStorage()
            ls.removeItem("practiceai_token")
            st.session_state.token = None
====
        if st.button("🚪 Logout", use_container_width=True):
            from streamlit_local_storage import LocalStorage
            ls = LocalStorage()
            ls.removeItem("agenticbuild_token")
            st.session_state.token = None
>>>>
```

- [ ] **Step 2: Commit changes**

```bash
git add frontend/components/sidebar.py
git commit -m "chore: update frontend/components/sidebar.py branding"
```

### Task 6: Final Verification and Cleanup

- [ ] **Step 1: Run grep to confirm no leftovers in the target files**

Run: `grep_search` with pattern `practiceai|PracticeAI` restricted to the 5 files.

- [ ] **Step 2: (Optional) Squashing commits if desired**
Since the task requested a specific commit message `chore: rebrand project to AgenticBuild`, I will perform a final commit/amend or squash if I committed along the way.
Actually, I will just commit all changes at the end with the requested message or follow the per-task commit and then rebase.
Actually, the user said: "Commit the changes with: `chore: rebrand project to AgenticBuild`".
I will perform the changes and then do a single commit at the end.

- [ ] **Step 3: Final commit**
```bash
git commit -m "chore: rebrand project to AgenticBuild"
```
