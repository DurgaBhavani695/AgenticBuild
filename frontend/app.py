import streamlit as st
from streamlit_local_storage import LocalStorage
from frontend.utils.api_client import APIClient
from frontend.components.auth_ui import render_auth_page
from frontend.components.sidebar import render_sidebar
from frontend.components.chat_ui import render_chat_interface

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
if "active_project" not in st.session_state:
    st.session_state.active_project = None
if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None
if "mode" not in st.session_state:
    st.session_state.mode = "project"

# --- CSS for modern Glassmorphism styling ---
st.markdown("""
<style>
    /* Global Background Fix */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Typography */
    h1, h2, h3, p, span, div {
        color: #f8fafc !important;
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b1120 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Button & Input Styling */
    .stButton button {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background: rgba(56, 189, 248, 0.1) !important;
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }
    
    /* Input Box styling */
    .stChatInputContainer {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Chat Container Area */
    .chat-container {
        max-height: 75vh;
        overflow-y: auto;
        padding: 20px;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    api_client = APIClient()
    
    # Sync token from session_state to local_storage if it was just set (e.g. after login)
    if st.session_state.token:
        local_storage.setItem("agenticbuild_token", st.session_state.token)
    
    if not st.session_state.token:
        render_auth_page()
    else:
        render_sidebar(api_client)
        render_chat_interface(api_client)

if __name__ == "__main__":
    main()
