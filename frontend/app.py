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
    /* Global Background and Typography */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        transition: transform 0.2s ease;
    }
    .stChatMessage:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Button & Input Styling */
    .stButton button {
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
    }
    
    /* Chat Container */
    .chat-container {
        max-height: 75vh;
        overflow-y: auto;
        padding: 20px;
        border-radius: 16px;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
    }
    
    /* Status Labels */
    .stStatus {
        background: rgba(56, 189, 248, 0.05) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 8px !important;
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
