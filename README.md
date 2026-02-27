<!-- python -m uvicorn app.server.auth:app --reload --port 8000 -->

# File Summarizing Agent

An intelligent Streamlit-powered agent that:

- Authenticates with Google
- Fetches files from Google Drive
- Summarizes them using OpenAI
- Displays and exports results

---

# Local Setup Guide

## 1. Clone the Repository

```bash
git clone https://github.com/sumayukh/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

## 2. Create venv

```bash
uv venv venv
```

## 2.1 Activate

If on Mac/Linux:

```bash
source venv/bin/activate
```

If on Windows:

```bash
venv/bin/activate
```

## 2.2 Install necessary dependencies

```bash
uv sync --active
```

OR if requirements.txt exists

```bash
uv add -r requirements.txt
```

# 3. Create .env

Create a .env file in the root directory. It should have the following keys with appropriate data.
GOOGLE_CLIENT_SECRET_FILE=Yourfile.json
TOKEN_FILE=Yourtokenfile.json
GOOGLE_READ_SCOPE_URI=Your read scope uri
GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/callback
OPENAI_API_KEY=Your OpenAI API key
FASTAPI_BACKEND_URL=http://localhost:8000

## 4. GCP setup

# 4.1 Go to: https://console.cloud.google.com/

# 4.2 Click Select Project → New Project

# 4.3 Name it → Create

# 4.4 Go to: APIs & Services → Library

# 4.5 Search: Google Drive API

# 4.6 Click Enable

# 4.7 APIs & Services → OAuth Consent Screen

# 4.8 Choose External

# 4.9 Fill ip the form and add SCOPE as https://www.googleapis.com/auth/drive.readonly

## 5. Oauth Credentials setup

# 5.1 Go to: https://console.cloud.google.com/

# 5.2 APIs & Services → Credentials

# 5.3 Click Create Credentials

# 5.4 Choose OAuth Client ID

# 5.5 Application Type: Web Application

# 5.6 Click Create

    You will get:

    **Client ID**

    **Client Secret**

    Download the JSON file and rename it into credentials.json after moving to the root directory of the project.

## 6. OPENAI setup

# 6.1 Go to https://platform.openai.com/

# 6.2 Create API Key

# 6.3 Paste the copied API Key into .env under OPENAI_API_KEY

## 7. Run the app(after venv is activated and packages are installed)

# 7.1 - Frontend(Streamlit) command: streamlit run main.py

# 7.2 - Backend(FastAPI) command: uvicorn app.server.auth:app --reload --port 8000
