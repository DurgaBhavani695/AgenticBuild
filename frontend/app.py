import streamlit as st
import requests

st.set_page_config(page_title="PracticeAI", layout="centered")

st.title("🤖 PracticeAI v1")
st.caption("Backend: FastAPI | LLM: Groq | Orchestration: LangGraph")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = requests.post(
                "http://localhost:8000/api/chat",
                json={"query": prompt}
            )
            response.raise_for_status()
            content = response.json()["response"]
            st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})
        except Exception as e:
            st.error(f"Error: {e}")
