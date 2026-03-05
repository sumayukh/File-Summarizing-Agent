import streamlit as st

def initialize_session():

    if "agent_state" not in st.session_state:

        st.session_state.agent_state = {
            "files": [],
            "loaded": False,
            "email": None,
            "access_token": None,
            "authenticated": False,
            "logs": []
        }

    if "has_run" not in st.session_state:
        st.session_state.has_run = False

def reset_session():
    st.session_state.agent_state = {
        "files": [],
        "loaded": False,
        "email": None,
        "access_token": None,
        "authenticated": False,
        "logs": []
    }

    st.session_state.has_run = False

    if "credentials" in st.session_state:
        del st.session_state["credentials"]

    st.rerun()