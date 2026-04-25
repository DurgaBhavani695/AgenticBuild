import streamlit as st

def render_chat_interface(api_client):
    active_project = st.session_state.get("active_project")
    active_session_id = st.session_state.get("active_session_id")
    mode = st.session_state.get("mode", "chat")
    
    st.title("🤖 AgenticBuild Workspace")
    
    if mode == "project" and active_project:
        st.info(f"🏗️ Project Context: **{active_project}**")
    elif active_session_id:
        st.info(f"💬 Continuing Session: **#{active_session_id}**")
    else:
        st.caption(f"Mode: **{mode.capitalize()}**")

    # Display history within a scrollable container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "preview_url" in message and message["preview_url"]:
                st.link_button("🌐 Open Live Preview", message["preview_url"])
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input
    if mode == "project":
        placeholder = "What are we building today?"
    else:
        placeholder = "How could I help you today?"
        
    if prompt := st.chat_input(placeholder):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            status_text = "🤖 Agent is thinking..." if mode == "chat" else "🤖 Agent is working..."
            with st.status(status_text) as status:
                try:
                    data = api_client.send_chat(
                        query=prompt,
                        mode=mode,
                        project_name=active_project,
                        session_id=active_session_id,
                        model_name=st.session_state.get("active_model")
                    )
                    
                    content = data["response"]
                    preview_url = data.get("preview_url")
                    new_session_id = data.get("session_id")
                    
                    st.markdown(content)
                    
                    if preview_url:
                        st.link_button("🌐 Open Live Preview", preview_url)
                    
                    new_msg = {"role": "assistant", "content": content}
                    if preview_url:
                        new_msg["preview_url"] = preview_url
                    
                    st.session_state.messages.append(new_msg)
                    
                    # Store session ID if it was just created
                    if new_session_id:
                        st.session_state.active_session_id = new_session_id
                    
                    # Update active project if it was just created
                    if data.get("project_name"):
                        st.session_state.active_project = data["project_name"]
                        
                    status.update(label="✅ Done!", state="complete")
                    
                    # If project was built or updated, refresh to see changes in sidebar
                    if mode == "project" or not active_session_id:
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error: {e}")
                    status.update(label="❌ Error", state="error")
