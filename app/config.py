import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CLIENT_SECRET_FILE = os.getenv("GOOGLE_CLIENT_SECRET_FILE")
TOKEN_FILE = os.getenv("TOKEN_FILE")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_READ_SCOPE_URI = os.getenv("GOOGLE_READ_SCOPE_URI")
FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL")
LOG_DIR = "logs"
FOLDER_NAME = "test"