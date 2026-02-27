import streamlit as st
import pandas as pd
from app.agents.graph import AgentGraph
import os

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
    if os.path.exists("token.json"):
        os.remove("token.json")
    st.rerun()

def ui():
    st.set_page_config(page_icon="random", page_title="AI File Summarizing Agent", layout="wide")
    st.title("AI File Summarizing Agent", anchor=False)

    st.subheader(
        """
            An intelligent Streamlit-powered agent that:
                - Authenticates with Google
                - Fetches files from Google Drive
                - Summarizes them using OpenAI
                - Displays and exports results
        """,
        anchor=False,
    )   
    
    if "agent_state" not in st.session_state:
        st.session_state.agent_state = {
            "files": [],
            "loaded": False,
            "email": None,
            "access_token": None,
            "authenticated": False,
            "logs": []
        }
        
    if st.session_state.get("has_run", False):
        st.session_state.has_run = False
        
    progress = st.progress(0)
    status = st.empty()
    col1, col2 = st.columns(2)
        
    
    
    with col1:
        start = st.button("Start", use_container_width=True)
    with col2:
        reset = st.button("Reset", use_container_width=True, disabled=not st.session_state.get("has_run", False))
        
    if start:
        try:
            status.info("Initializing agent...")
            progress.progress(20)
            
            graph = AgentGraph().build_graph()
            
            state = {
                "files": [],
                "loaded": False,
                "email": None,
                "access_token": None,
                "authenticated": False,
                "logs": []
            }
            
            status.info("Running authentication check...")
            progress.progress(40)
            
            for stage in graph.stream(state):
                state = list(stage.values())[0]
                logs = state.get("logs", [])
                progress.progress(min(len(logs) * 10, 90))
                status.info(logs[-1] if len(logs) > 0 else "Processing...")
        
            progress.progress(100)
            st.session_state.agent_state = state
            st.session_state.has_run = True
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
                
    
    if reset:
        reset_session()
    
    if st.session_state.get("has_run", False) == True:
        state = st.session_state.agent_state
        
        if len(state.get("files", [])) > 0:
            df = pd.DataFrame(state["files"])
            st.dataframe(df[["name", "summary"]])
        else:
            st.warning("No files were summarized.")
                
        with st.expander("Process Logs"):
            logs = state.get("logs", [])
            [st.write(log) for log in logs] if len(logs) > 0 else st.write("No logs available.")