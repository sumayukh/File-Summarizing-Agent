from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json
import streamlit as st
from app.config import GOOGLE_CLIENT_SECRET_FILE, GOOGLE_READ_SCOPE_URI, GOOGLE_REDIRECT_URI

SCOPES = [GOOGLE_READ_SCOPE_URI]


def init_oauth_flow():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES
    )

    flow.redirect_uri = GOOGLE_REDIRECT_URI
    return flow

def login():
    try:
        flow = init_oauth_flow()

        auth_url, _ = flow.authorization_url(
            access_type="offline",
            prompt="consent",
            include_granted_scopes="true"
        )

        return auth_url
    except Exception as e:
        return None

def oauth_callback(code):
    try:
        flow = init_oauth_flow()

        if not code:
            return None

        flow.fetch_token(code=code)
        creds = flow.credentials
        credentials = get_credentials_dict(creds)

        return credentials
    except Exception as e:
        return None
    
def get_credentials_dict(credentials):
    return json.loads(credentials.to_json())

def authenticate():
    try:
        credentials = st.session_state.get("credentials")

        if not credentials:
            return None, None
        
        creds = Credentials.from_authorized_user_info(credentials)
        
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            credentials = get_credentials_dict(creds)

        return credentials, creds
    except Exception as e:
        return None, None