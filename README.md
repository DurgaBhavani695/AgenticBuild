# AgenticBuild 🤖
**Autonomous Full-Stack AI Engineer**

AgenticBuild is an AI platform that builds web applications and scripts from natural language. It uses **Agentic Loops** to architect, write, and automatically fix code until it works.

---

## 🖼️ Visual Gallery
*Examples of the AgenticBuild workspace and applications built by the agent.*

<div align="center">
  <img src="docs/assets/screenshots/screenshot-1.jpeg" width="45%" alt="AgenticBuild Dashboard"/>
  <img src="docs/assets/screenshots/screenshot-2.jpeg" width="45%" alt="AI Reasoning Process"/>
</div>
<div align="center">
  <img src="docs/assets/screenshots/screenshot-3.jpeg" width="45%" alt="Generated Weather App - Overview"/>
  <img src="docs/assets/screenshots/screenshot-4.jpeg" width="45%" alt="Generated Weather App - Detail"/>
</div>

---

## ✨ Key Features

### 🧠 Smart Building
- **Self-Healing Code**: If the code has bugs, the agent detects and fixes them automatically before showing you the result.
- **Incremental Updates**: You can add features or change styling on an existing project just by asking.
- **Smart Fallback**: If a complex design is too large for the AI, it automatically switches to a robust single-file version so you always get a working app.
- **Feasibility Check**: The agent analyzes your request first and suggests simpler alternatives if it hits a technical limit.

### 🛠️ Workspace & Tools
- **Multiple Sessions**: Work on different projects at the same time without losing progress.
- **Model Switching**: Easily switch between different AI models (Llama 4, OpenAI 120B, etc.) in the middle of a chat.
- **ZIP Exports**: Download your completed projects as a ZIP file directly from the sidebar.
- **Secure Access**: Private user accounts with JWT authentication to keep your projects isolated.

---

## 🚀 Quick Start

### 1. Setup
```bash
pip install uv
uv sync
```

### 2. Configuration
Create a `.env` file from `.env.example`:
```env
GROQ_API_KEY=your_key_here
```

### 3. Run
```bash
uv run python init_and_run.py
```

---

## 🛠️ Development Methodology
Built using an **AI-First** approach:
- **Tools**: Developed using Gemini CLI and Superpowers MCP for research and planning.
- **Process**: Followed a "Design before Code" workflow to keep the architecture clean.
- **Human Synergy**: AI handles the heavy implementation, while I focus on high-level system design and security.

---

## 🏗️ Technical Stack
- **Backend**: Python 3.14, FastAPI, SQLModel (SQLite)
- **AI Brain**: LangGraph, LangChain, Groq
- **Frontend**: Streamlit, Tailwind CSS, GSAP
- **Capabilities**: Single-Page Apps (Three.js/GSAP) and Python Scripts

---

## 🚧 Roadmap & Security (TODO)
- [ ] **UI Polish**: Tighten up visual consistency and fix minor UI bugs.
- [ ] **Prompt Security**: Add layers to prevent prompt injection and malicious usage.
- [ ] **Sandboxing**: Run generated code in a safe, isolated environment.
- [ ] **Code Auditing**: Automatically scan generated code for security vulnerabilities.
