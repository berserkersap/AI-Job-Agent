# multi_agent_main.py

import os
from typing import List, TypedDict, Optional

# --- Assume all our modules are available ---
from modules import (
    input_handler, 
    analysis_engine, 
    job_searcher, 
    application_automator, 
    user_interface, 
    rag_engine
)
from langgraph.graph import StateGraph, END

# --- 1. Define the Agent State  ---
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

# --- 2. Define the Agent Nodes ---

def search_agent_node(state: AgentState) -> AgentState:
    """Agent responsible for searching for jobs."""
    print("--- AGENT: Searcher ---")
    print("Expanding job search...")
    expanded_titles = analysis_engine.expand_job_titles(state["job_query"])
    print(f"Searching for: {expanded_titles}")
    
    found_jobs = job_searcher.search_jobs(expanded_titles, state["location"])
    
    return {**state, "expanded_job_titles": expanded_titles, "found_jobs": found_jobs}

def analysis_agent_node(state: AgentState) -> AgentState:
    """Agent responsible for analyzing and ranking jobs."""
    print("\n--- AGENT: Analyst ---")
    print("Analyzing jobs against your resume...")
    analyzed_jobs = []
    resume_text = state["resume_text"]
    
    for job in state["found_jobs"]:
        score, _ = analysis_engine.compare_resume_to_jd(resume_text, job.get('description', ''))
        job['match_score'] = score
        analyzed_jobs.append(job)
        
    analyzed_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    return {**state, "analyzed_jobs": analyzed_jobs}

def user_proxy_agent_node(state: AgentState) -> AgentState:
    """Agent that interacts with the user for selection."""
    print("\n--- AGENT: User Proxy ---")
    user_interface.display_jobs(state["analyzed_jobs"])
    selected_jobs = user_interface.get_user_selections(state["analyzed_jobs"])
    
    if not selected_jobs:
        print("User selected no jobs. Ending process.")
        return {**state, "selected_jobs": []}

    # Build the RAG chain for the next step
    selected_jds = [job['description'] for job in selected_jobs]
    rag_chain = rag_engine.create_rag_chain(state["resume_text"], selected_jds)
    
    return {**state, "selected_jobs": selected_jobs, "rag_chain": rag_chain}

def application_agent_node(state: AgentState) -> AgentState:
    """Agent that applies to the selected jobs."""
    print("\n--- AGENT: Applicator ---")
    rag_chain = state["rag_chain"]
    
    for job in state["selected_jobs"]:
        print(f"\nProcessing application for: {job['title']} at {job['company']}")
        
        print("\n--- RAG-Powered Resume Suggestions ---")
        suggestions = rag_engine.query_rag_chain(rag_chain, job['title'])
        print(suggestions)
        print("-" * 20)
        
        use_default = input("Use the default resume? (y/n): ").lower()
        current_resume_path = state["default_resume_path"]
        if use_default != 'y':
            custom_resume = input("Enter path to tailored resume: ")
            current_resume_path = custom_resume if os.path.exists(custom_resume) else state["default_resume_path"]
        
        application_automator.apply_to_job(job['url'], current_resume_path)
    
    return state # No state change needed here

# --- 3. Define the Graph and Edges ---

workflow = StateGraph(AgentState)

# Add nodes to the graph
workflow.add_node("searcher", search_agent_node)
workflow.add_node("analyst", analysis_agent_node)
workflow.add_node("user_proxy", user_proxy_agent_node)
workflow.add_node("applicator", application_agent_node)

# Define the flow of control (edges)
workflow.set_entry_point("searcher")
workflow.add_edge("searcher", "analyst")
workflow.add_edge("analyst", "user_proxy")

# Add a conditional edge
def decide_to_apply(state: AgentState):
    """Decides whether to proceed to application or end."""
    if state.get("selected_jobs") and len(state["selected_jobs"]) > 0:
        return "applicator"
    else:
        return END

workflow.add_conditional_edges(
    "user_proxy",
    decide_to_apply,
    {"applicator": "applicator", END: END}
)
workflow.add_edge("applicator", END) # End after applying

# Compile the graph into a runnable app
app = workflow.compile()

# --- 4. Run the Multi-Agent System ---
if __name__ == "__main__":
    resume_path, desired_job, location = user_interface.get_initial_input()
    resume_text = input_handler.parse_resume(resume_path)

    if resume_text:
        initial_state = AgentState(
            resume_text=resume_text,
            default_resume_path=resume_path,
            job_query=desired_job,
            location=location
        )
        # Run the graph
        final_state = app.invoke(initial_state)
        print("\n\n✅ Multi-agent workflow complete.")
