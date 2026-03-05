import streamlit as st
import pandas as pd
from app.agents.graph import AgentGraph
from app.session import reset_session


def render_summarizer():
    
    if "credentials" not in st.session_state:
        st.warning("Please authenticate first.")
        return
        # st.switch_page("/oauth")

    if "agent_state" not in st.session_state:
        st.session_state.agent_state = {
            "files": [],
            "loaded": False,
            "email": None,
            "access_token": None,
            "authenticated": False,
            "logs": []
        }

    progress = st.progress(0)
    status = st.empty()

    col1, col2 = st.columns(2)

    with col1:
        start = st.button("Start", use_container_width=True)

    with col2:
        reset = st.button(
            "Reset",
            use_container_width=True,
            disabled=bool(st.session_state.get("access_token", False))
        )

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
            for stage in graph.stream(state):
                state = list(stage.values())[0]
                logs = state.get("logs", [])
                progress.progress(min(len(logs) * 10, 90))
                status.info(logs[-1] if logs else "Processing...")

            progress.progress(100)
            st.session_state.agent_state = state
            st.session_state.has_run = True

        except Exception as e:
            st.error(f"Agent execution failed: {str(e)}")

    if reset:
        reset_session()

    if st.session_state.get("has_run"):
        state = st.session_state.agent_state
        if len(state.get("files", [])) > 0:
            df = pd.DataFrame(state["files"])
            st.dataframe(df[["name", "summary"]])
        else:
            st.warning("No files were summarized.")
        with st.expander("Process Logs"):
            logs = state.get("logs", [])
            [st.write(log) for log in logs] if logs else st.write("No logs available.")
            
if __name__ == "__main__":
    render_summarizer()