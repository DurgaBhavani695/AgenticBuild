import streamlit as st

def render_sidebar(api_client):
    with st.sidebar:
        st.title("⚙️ AgenticBuild Settings")
        
        # User Info & Logout
        if st.button("🚪 Logout", use_container_width=True):
            from streamlit_local_storage import LocalStorage
            ls = LocalStorage()
            ls.removeItem("agenticbuild_token")
            st.session_state.token = None
            st.session_state.messages = []
            st.session_state.active_project = None
            st.session_state.active_session_id = None
            st.rerun()

        st.divider()

        # Model Selection
        model_options = {
            "OpenAI 120B (Groq)": "openai/gpt-oss-120b",
            "OpenAI 20B (Groq)": "openai/gpt-oss-20b",
            "Llama 3.3 70B (Groq)": "llama-3.3-70b-versatile",
            "Llama 4 Scout 17B (Groq)": "meta-llama/llama-4-scout-17b-16e-instruct",
            "Groq Compound": "groq/compound",
            "Groq Compound Mini": "groq/compound-mini"
        }
        
        # Determine default index from backend config if not already set
        if "active_model" not in st.session_state:
            config = api_client.get_config()
            default_model = config.get("default_model") if config else "openai/gpt-oss-120b"
            
            # Find matching index
            default_index = 0
            for i, (label, val) in enumerate(model_options.items()):
                if val == default_model:
                    default_index = i
                    break
            st.session_state.active_model = default_model
            st.session_state.model_index = default_index
        else:
            # Keep existing index if user already manually selected something
            default_index = st.session_state.get("model_index", 0)

        selected_model_label = st.selectbox(
            "🚀 Active Model:",
            options=list(model_options.keys()),
            index=default_index,
            key="model_selector"
        )
        st.session_state.active_model = model_options[selected_model_label]
        # Store index to preserve selection across reruns
        st.session_state.model_index = list(model_options.keys()).index(selected_model_label)
        st.caption(f"Currently using: `{st.session_state.active_model}`")

        st.divider()
        app_mode = st.radio(
            "Select Mode:",
            ["💬 Chat", "🏗️ Build Project"],
            index=1 if st.session_state.get("mode") == "project" else 0,
            key="mode_radio_v3"
        )
        
        # --- Handle Mode Change Side Effects ---
        new_mode = "project" if app_mode == "🏗️ Build Project" else "chat"
        if st.session_state.get("mode") != new_mode:
            st.session_state.mode = new_mode
            st.session_state.active_project = None
            st.session_state.active_session_id = None
            st.session_state.messages = []
            st.rerun()
        
        if st.button("➕ New Session", use_container_width=True):
            st.session_state.messages = []
            st.session_state.active_project = None
            st.session_state.active_session_id = None
            st.rerun()

        st.divider()
        
        if st.session_state.mode == "chat":
            st.header("💬 Chat History")
            sessions = api_client.get_sessions()
            chat_sessions = [s for s in sessions if s.get("project_id") is None]
            
            if not chat_sessions:
                st.info("No chat history.")
            for sess in chat_sessions:
                is_active = st.session_state.get("active_session_id") == sess["id"]
                
                with st.expander(f"{'⭐ ' if is_active else '💬 '}{sess['name'][:25]}", expanded=is_active):
                    if is_active:
                        st.success("Currently Active")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("💬 Open", key=f"open_{sess['id']}", use_container_width=True):
                            st.session_state.active_session_id = sess["id"]
                            st.session_state.active_project = None
                            st.session_state.messages = api_client.get_session_messages(sess["id"])
                            st.rerun()
                    with c2:
                        if st.button("🗑️ Delete", key=f"del_sess_{sess['id']}", use_container_width=True):
                            if api_client.delete_session(sess["id"]):
                                if st.session_state.get("active_session_id") == sess["id"]:
                                    st.session_state.active_session_id = None
                                    st.session_state.messages = []
                                st.toast("Session deleted")
                                st.rerun()
        else:
            st.header("📂 Projects")
            sessions = api_client.get_sessions()
            project_sessions = [s for s in sessions if s.get("project_id") is not None]
            
            if not project_sessions:
                st.info("No projects yet.")
            for sess in project_sessions:
                is_active = st.session_state.get("active_session_id") == sess["id"]
                p_name = sess["name"]
                
                # --- Highlighting and Delete ---
                with st.expander(f"{'⭐ ' if is_active else '📁 '}{p_name}", expanded=is_active):
                    if is_active:
                        st.success("Currently Active")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🎯 Activate", key=f"act_{sess['id']}", use_container_width=True):
                            st.session_state.active_session_id = sess["id"]
                            st.session_state.active_project = p_name
                            st.session_state.messages = api_client.get_session_messages(sess["id"])
                            st.rerun()
                    with c2:
                        if st.button("🗑️ Delete", key=f"del_proj_{sess['id']}", use_container_width=True):
                            if api_client.delete_project(p_name):
                                if st.session_state.get("active_project") == p_name:
                                    st.session_state.active_project = None
                                    st.session_state.active_session_id = None
                                    st.session_state.messages = []
                                st.toast(f"Deleted {p_name}")
                                st.rerun()
                    
                    details = api_client.get_project_details(p_name)
                    if details:
                        st.caption("📄 Files in Project:")
                        st.text("\n".join(details.get("files", [])))
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if "index.html" in details.get("files", []):
                                preview_url = f"http://localhost:8000/view-projects/{p_name}/index.html"
                                st.link_button("🌐 Preview", preview_url, use_container_width=True)
                        with c2:
                            # Use binary download for ZIP
                            zip_data = api_client.download_project(p_name)
                            if zip_data:
                                st.download_button(
                                    label="📥 ZIP",
                                    data=zip_data,
                                    file_name=f"{p_name}.zip",
                                    mime="application/zip",
                                    use_container_width=True,
                                    key=f"dl_{sess['id']}"
                                )
