from typing import List, Dict, TypedDict, Optional

class AgentState(TypedDict):
    files: List[Dict]
    loaded: bool
    email: Optional[str]
    access_token: Optional[str]
    authenticated: bool
    logs: List[str]