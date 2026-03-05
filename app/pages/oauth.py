import streamlit as st
from app.tools.auth import login, oauth_callback

def render_oauth():
    st.subheader("""
                 Google Authentication
                    - Click on the button below. It will open a new tab
                    - Once it opens, you may close this tab.
                """, anchor=False)
    
    try:
        if "credentials" not in st.session_state:
            query_params = st.query_params
            if "code" not in query_params:
                auth_url = login()
                st.link_button("Login with Google", url=auth_url)
            else:
                code = query_params.get("code")
                credentials = oauth_callback(code)
                if credentials:
                    st.session_state["credentials"] = credentials
                    st.query_params.clear()
                    st.success("Authentication successful.")
                    st.rerun()
                else:
                    st.error("Authentication failed")
        else:
            st.success("Already authenticated")
            return

    except Exception as e:
        st.error(f"OAuth error: {str(e)}")
        
if __name__ == "__main__":
    render_oauth()