import streamlit as st
from app.session import initialize_session
from app.layout import render_layout
from app.pages.oauth import render_oauth
from app.pages.summarizer import render_summarizer

@st.fragment
def render_route():
    
    if st.session_state.get("credentials"):
        return render_summarizer
    
    return render_oauth


def main():

    initialize_session()
    child = render_route()
    render_layout(child)

if __name__ == "__main__":
    main()