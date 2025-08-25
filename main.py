# main.py
import os
from modules import input_handler, analysis_engine, job_searcher, application_automator, user_interface

def main_workflow():
    # 1. Get User Input
    default_resume_path, desired_job, location = user_interface.get_initial_input()
    resume_text = input_handler.parse_resume(default_resume_path)
    if not resume_text:
        print("Could not read resume. Exiting.")
        return

    # 2. Expand Job Search
    print("\n🧠 Expanding job search to related roles...")
    expanded_titles = analysis_engine.expand_job_titles(desired_job)

    # 3. Search for Jobs
    job_listings = job_searcher.search_jobs(expanded_titles, location)

    # 4. Analyze and Rank Jobs
    analyzed_jobs = []
    print("\n🔬 Analyzing job descriptions against your resume...")
    for job in job_listings:
        score, _ = analysis_engine.compare_resume_to_jd(resume_text, job.get('description', ''))
        job['match_score'] = score
        if score < 0.2: # Threshold for suggesting resume changes
            job['suggestions'] = "High skill gap. Consider tailoring your resume significantly."
        analyzed_jobs.append(job)

    # Sort jobs by match score in descending order
    analyzed_jobs.sort(key=lambda x: x['match_score'], reverse=True)

    # 5. Display jobs and get user selection
    user_interface.display_jobs(analyzed_jobs)
    selected_jobs = user_interface.get_user_selections(analyzed_jobs)
    
    if not selected_jobs:
        print("No jobs selected for application. Exiting.")
        return

    # 6. Process Applications for Selected Jobs
    print("\n--- 🚀 Preparing to Apply ---")
    for job in selected_jobs:
        print(f"\nProcessing application for: {job['title']} at {job['company']}")
        
        # Suggest resume tailoring
        suggestions = analysis_engine.generate_resume_suggestions(resume_text, job.get('description', ''))
        print("\n--- AI Resume Suggestions ---")
        print(suggestions)
        print("--------------------------")
        
        use_default = input("Use the default resume for this application? (y/n): ").lower()
        current_resume_path = default_resume_path
        if use_default != 'y':
            custom_resume = input("Enter path to tailored resume for this job: ")
            if os.path.exists(custom_resume):
                current_resume_path = custom_resume
            else:
                print("Custom resume not found. Using default.")

        # For this example, we assume no cover letter is needed.
        # A real version would prompt for this.
        application_automator.apply_to_job(job['url'], current_resume_path)

    # 8. Post-Application Feedback
    print("\n\n--- 🌟 Career Development Suggestions ---")
    skills_to_learn = analysis_engine.suggest_skills_to_learn(resume_text, desired_job)
    print(skills_to_learn)
    print("\nAll tasks completed. Good luck with your job hunt! 💪")

if __name__ == "__main__":
    main_workflow()
