from langgraph.graph import StateGraph
from app.agents.state import AgentState
from app.tools.auth import authenticate
from app.tools.g_drive import GDriveService
from app.tools.parse import ParserService
from app.utils.logger import Logger
from app.tools.summarize import SummarizerService
from app.config import FASTAPI_BACKEND_URL, FOLDER_NAME
import json
import os
import webbrowser
import time

summarizer = SummarizerService()
logger = Logger()

def print_log(state: AgentState, message: str):
    logger.log(message)
    state["logs"].append(message)

def auth_check_node(state: AgentState):
    print_log(state, "Checking authentication status...")
    credentials = authenticate()
    
    if not credentials:
        state["authenticated"] = False
        print_log(state, "User not authenticated.")
        return state
    
    state["authenticated"] = True
    state["access_token"] = credentials.token
    email = None
    if hasattr(credentials, "id_token") and credentials.id_token:
        email = credentials.id_token.get("email", None)
        
    state["email"] = email
    print_log(state, f"User authenticated: {state['email']}")
    
    return state
    
def login_node(state: AgentState):
    print_log(state, "No stored credentials found.")
    print_log(state, "Opening browser for first-time authentication...")
    loginUrl = f"{FASTAPI_BACKEND_URL}/login"
    webbrowser.open(loginUrl)
    
    raise Exception("First-time login required. Complete authentication in browser and click Start again.")

def read_node(state: AgentState):
    
    print_log(state, "Accessing Google Drive...")
    credentials = authenticate()
    if not credentials:
        raise Exception("Authentication required before reading files.")
    
    drive = GDriveService(credentials)
    print_log(state, f"Searching for folder: {FOLDER_NAME}")
    
    folder_id = None
    
    try:
        folder_id = drive.get_folder_id(FOLDER_NAME)
        print_log(state, "Folder detected.")
    except Exception as _:
        print_log(state, "No folder found.")
        state["loaded"] = False
        return state
    
    print_log(state, "Listing files...")
    files = drive.list_files(folder_id)
    if not files:
        print_log(state, "No files found in folder.")
        state["loaded"] = False
        return state
    
    print_log(state, f"{len(files)} files detected.")
    print_log(state, "Parsing data...")
    
    parsed_files = []
    
    for file in files:
        parsed_file = {}
        mime_type = file["mimeType"]
        
        if mime_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain"
        ]:
            continue
        
        print_log(state, f"Downloading: {file['name']}")
        
        file_stream = drive.download_file(file["id"])
        parser = ParserService(file_stream, mime_type)
        data = parser.parse_file()
        parsed_file["name"] = file["name"]
        parsed_file["data"] = data
        parsed_file["summary"] = ""
        parsed_files.append(parsed_file)
        
    state["files"] = parsed_files
    state["loaded"] = True
    
    print_log(state, f"{len(parsed_files)} files read successfully.")
    
    return state
        

def write_node(state: AgentState):
    if not state["loaded"]:
        print_log(state, "No files to summarize.")
        return state

    print_log(state, "Summarizing data...")

    for file in state["files"]:
        try:
            summary = summarizer.summarize(file["data"])
            file["summary"] = summary
            print_log(state, f"Summarized: {file['name']}")
            time.sleep(3)
        except Exception as e:
            print_log(state, f"Error summarizing {file['name']}: {str(e)}")

    os.makedirs("reports", exist_ok=True)

    with open("reports/output.json", "w") as f:
        json.dump(state["files"], f, indent=4)
        
    summarized_files = [f for f in state["files"] if f.get("summary", "").strip() != ""]
    print_log(state, f"{len(summarized_files)} files summarized successfully.") if len(summarized_files) > 0 else print_log(state, "No files were summarized.")
    return state

class AgentGraph:
    def build_graph(self):
        graph = StateGraph(AgentState)

        graph.add_node("auth_check", auth_check_node)
        graph.add_node("login", login_node)
        graph.add_node("read", read_node)
        graph.add_node("write", write_node)

        graph.set_entry_point("auth_check")

        graph.add_conditional_edges("auth_check", lambda state: "login" if not state["authenticated"] else "read")
        
        graph.add_edge("login", "read")
        graph.add_edge("read", "write")
        # graph.add_edge("write", "END")

        return graph.compile()