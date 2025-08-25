# modules/job_searcher.py
# IMPORTANT: This is a MOCK searcher. Real web scraping is complex and
# can be against a website's terms of service. Always use official APIs when available.

def search_jobs(job_titles, location):
    """MOCK FUNCTION: Simulates searching for jobs and returning a list."""
    print(f"🔍 Searching for {job_titles} jobs in {location}...")
    
    # In a real implementation, you would use libraries like requests and BeautifulSoup
    # or a dedicated API (e.g., LinkedIn API, if you have access) to get job data.
    
    mock_jobs = [
        {
            "title": "Senior Data Scientist",
            "company": "Innovate AI Inc.",
            "location": location,
            "url": "https://www.linkedin.com/jobs/view/12345",
            "description": "Innovate AI is seeking a Senior Data Scientist with experience in Python, TensorFlow, and cloud platforms. You will develop machine learning models to solve complex business problems."
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Tech Solutions LLC",
            "location": location,
            "url": "https://www.indeed.com/viewjob?jk=67890",
            "description": "We are looking for an ML Engineer proficient in PyTorch, scikit-learn, and SQL. Experience with Natural Language Processing (NLP) is a huge plus. This role involves deploying models to production."
        },
        {
            "title": "Junior Gen AI Engineer",
            "company": "Future Forward",
            "location": location,
            "url": "https://careers.futureforward.com/job/11223",
            "description": "Entry-level position for a Gen AI Engineer. Must have a foundational understanding of large language models (LLMs), Python, and basic deep learning concepts. No professional experience in AWS is required, but it is a bonus."
        }
    ]
    
    # Filter mock jobs to somewhat match the input titles
    found_jobs = [job for job in mock_jobs if any(title.split()[0].lower() in job['title'].lower() for title in job_titles)]
    
    print(f"✅ Found {len(found_jobs)} mock jobs.")
    return found_jobs
