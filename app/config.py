import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
GOOGLE_CLIENT_SECRET_FILE = os.getenv("GOOGLE_CLIENT_SECRET_FILE") or st.secrets["GOOGLE_CLIENT_SECRET_FILE"]
TOKEN_FILE = os.getenv("TOKEN_FILE") or st.secrets["TOKEN_FILE"]
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI") or st.secrets["GOOGLE_REDIRECT_URI"]
GOOGLE_READ_SCOPE_URI = os.getenv("GOOGLE_READ_SCOPE_URI") or st.secrets["GOOGLE_READ_SCOPE_URI"]
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL") or st.secrets["GROQ_BASE_URL"]
LOG_DIR = "logs"
FOLDER_NAME = "test"