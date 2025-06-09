import streamlit as st

def render_sidebar():
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

        return uploaded_file, file_content, file_name
