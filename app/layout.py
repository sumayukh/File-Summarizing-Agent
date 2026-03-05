import streamlit as st

def render_layout(child):
    if "layout_rendered" not in st.session_state:
        st.set_page_config(page_icon="random", page_title="AI File Summarizing Agent", layout="wide")

    st.title("AI File Summarizing Agent", anchor=False)

    st.subheader(
        """
        An intelligent Streamlit-powered agent that:
        - Authenticates with Google
        - Fetches files from Google Drive's "test" folder
        - Summarizes them using OpenAI
        - Displays and exports results
        """,
        anchor=False,
    )

    st.session_state.layout_rendered = True
    
    child_container = st.container()
    with child_container:
        child()