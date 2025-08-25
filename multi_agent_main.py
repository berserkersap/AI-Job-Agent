# multi_agent_main.py (New File)
from typing import List, TypedDict, Optional

class AgentState(TypedDict):
    """Represents the shared state of our agent system."""
    resume_text: str
    default_resume_path: str
    job_query: str
    location: str
    expanded_job_titles: Optional[List[str]]
    found_jobs: Optional[List[dict]]
    analyzed_jobs: Optional[List[dict]]
    selected_jobs: Optional[List[dict]]
    final_feedback: str
