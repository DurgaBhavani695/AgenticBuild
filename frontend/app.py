import streamlit as st
from streamlit_local_storage import LocalStorage
from frontend.utils.api_client import APIClient
from frontend.components.auth_ui import render_auth_page
from frontend.components.sidebar import render_sidebar
from frontend.components.chat_ui import render_chat_interface

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
if "active_project" not in st.session_state:
    st.session_state.active_project = None
if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None
if "mode" not in st.session_state:
    st.session_state.mode = "project"

# --- CSS for better styling ---
st.markdown("""
<style>
    .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    .stButton button { width: 100%; }
    
    /* Chat message container styling */
    .chat-container {
        max-height: 70vh;
        overflow-y: auto;
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
    }
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    api_client = APIClient()
    
    # Sync token from session_state to local_storage if it was just set (e.g. after login)
    if st.session_state.token:
        local_storage.setItem("practiceai_token", st.session_state.token)
    
    if not st.session_state.token:
        render_auth_page()
    else:
        render_sidebar(api_client)
        render_chat_interface(api_client)

if __name__ == "__main__":
    main()
