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
git clone https://github.com/sumayukh/File-Summarizing-Agent.git
cd File-Summarizing-Agent
code .
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

- GOOGLE_CLIENT_SECRET_FILE=Yourfile.json
- TOKEN_FILE=Yourtokenfile.json
- GOOGLE_READ_SCOPE_URI=Your read scope uri
- GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/callback
- OPENAI_API_KEY=Your OpenAI API key
- GROQ_BASE_URL=https://api.groq.com/openai/v1
- FASTAPI_BACKEND_URL=http://localhost:8000

## 4. GCP setup

- Go to: https://console.cloud.google.com/
- Click Select Project → New Project
- Name it → Create
- Go to: APIs & Services → Library
- Search: Google Drive API
- Click Enable
- APIs & Services → OAuth Consent Screen
- Choose External
- Fill ip the form and add SCOPE as https://www.googleapis.com/auth/drive.readonly

## 5. Oauth Credentials setup

- Go to: https://console.cloud.google.com/
- APIs & Services → Credentials
- Click Create Credentials
- Choose OAuth Client ID
- Application Type: Web Application
- Click Create

  You will get:

        - **Client ID**
        - **Client Secret**

  Download the JSON file and rename it into credentials.json after moving to the root directory of the project.

## 6. OPENAI setup

- Go to https://platform.openai.com/
- Create API Key
- Paste the copied API Key into .env under OPENAI_API_KEY
- Run the app(after venv is activated and packages are installed)
- Frontend(Streamlit) command - streamlit run main.py
- Backend(FastAPI) command - uvicorn app.server.auth:app --reload --port 8000
