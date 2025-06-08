import streamlit as st
from backend_interface import BackendInterface

#This file handles UI layout using Streamlit

st.set_page_config(page_title="SLAM - Smart Language Agentic Machine", page_icon="🤖", layout="wide")

agent_api = BackendInterface()

# Session state setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

if st.session_state.clear_input:
    st.session_state.input = ""
    st.session_state.clear_input = False

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ SLAM Controls")
    uploaded_file = st.file_uploader("Attach a file (optional):", type=["txt", "pdf", "docx"])
    file_content = ""
    file_name = ""

    if uploaded_file is not None:
        file_name = uploaded_file.name
        try:
            file_content = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    if st.button("🔄 New Chat"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Title
st.title("🤖 SLAM")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input (fixed bottom)
user_input = st.chat_input("Ask the agent something...")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if uploaded_file is not None:
                response = f"File uploaded: `{file_name}`"
            else:
                result = agent_api.get_agent_response(user_input, file_content)
                response = result["response"]

            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
