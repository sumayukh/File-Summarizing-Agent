from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
import os
from app.config import GOOGLE_CLIENT_SECRET_FILE, GOOGLE_REDIRECT_URI, GOOGLE_READ_SCOPE_URI, TOKEN_FILE

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [GOOGLE_READ_SCOPE_URI]

app = FastAPI()

@app.get("/login")
def login():
    flow = Flow.from_client_secrets_file(GOOGLE_CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline", include_granted_scopes="true")
    
    return RedirectResponse(auth_url)

@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    flow = Flow.from_client_secrets_file(GOOGLE_CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    authorization_response = str(request.url)
    
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    with open(TOKEN_FILE, "w") as token:
        token.write(credentials.to_json())
        
    return {"message": "Authentication successful. You may return to Streamlit."}

@app.get("/logout")
def logout():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    return {"message": "Logged out successfully"}