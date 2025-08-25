# modules/user_interface.py
import os

def get_initial_input():
    """Gets initial information from the user."""
    print("--- 🤖 Welcome to the AI Job Application Agent ---")
    resume_path = input("Enter the full path to your resume file: ")
    while not os.path.exists(resume_path):
        print("File not found. Please try again.")
        resume_path = input("Enter the full path to your resume file: ")
        
    desired_job = input("Enter your desired job title (e.g., 'Data Scientist'): ")
    location = input("Enter your desired location (e.g., 'Chennai, India'): ")
    return resume_path, desired_job, location

def display_jobs(job_list):
    """Displays the ranked list of jobs."""
    print("\n--- 📊 Here are the top job matches for you ---")
    if not job_list:
        print("No jobs found.")
        return
        
    for i, job in enumerate(job_list, 1):
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Match Score: {job['match_score'] * 100:.0f}% {' düşük eşleşme' if job['match_score'] < 0.2 else ''}")
        print(f"   Location: {job['location']}")
        print(f"   URL: {job['url']}")
        if job.get('suggestions'):
            print(f"   💡 Resume Tip: {job['suggestions']}")
        print("-" * 20)

def get_user_selections(job_list):
    """Asks the user to select which jobs to apply for."""
    if not job_list:
        return []
        
    selections = input("\nEnter the numbers of the jobs you want to apply for (comma-separated), or 'q' to quit: ")
    if selections.lower() == 'q':
        return []
        
    selected_indices = [int(i.strip()) - 1 for i in selections.split(',')]
    selected_jobs = [job_list[i] for i in selected_indices if 0 <= i < len(job_list)]
    return selected_jobs
