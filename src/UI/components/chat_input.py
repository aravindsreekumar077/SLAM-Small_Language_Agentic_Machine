import streamlit as st

def render_chat_input(agent_api, uploaded_file, file_content, file_name):
    if st.session_state.clear_input:
        st.session_state.input = ""
        st.session_state.clear_input = False

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
