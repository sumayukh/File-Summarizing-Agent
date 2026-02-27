from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from app.config import TOKEN_FILE, GOOGLE_READ_SCOPE_URI

SCOPES = [GOOGLE_READ_SCOPE_URI]


def authenticate():
    if not os.path.exists(TOKEN_FILE):
        return None

    try:
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            with open(TOKEN_FILE, "w") as token:
                token.write(credentials.to_json())

        return credentials
    except Exception as e:
        return None