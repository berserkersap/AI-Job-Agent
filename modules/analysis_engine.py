# modules/analysis_engine.py
from langchain_google_genai import ChatGoogleGenerativeAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import config

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=config.GOOGLE_API_KEY)

def expand_job_titles(desired_job):
    """Uses LLM to find related job titles."""
    prompt = f"""
    Given the desired job title "{desired_job}", list 5 similar or related job titles.
    Return the list as a comma-separated string. For example: Job A, Job B, Job C
    """
    response = llm.invoke(prompt)
    expanded_titles = [title.strip() for title in response.content.split(',')]
    return [desired_job] + expanded_titles

def compare_resume_to_jd(resume_text, jd_text):
    """Compares resume to job description using TF-IDF and Cosine Similarity."""
    if not resume_text or not jd_text:
        return 0, []

    texts = [resume_text, jd_text]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Calculate cosine similarity
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Simple skill gap analysis (can be improved with NER)
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    missing_skills = list(jd_words - resume_words) # This is a simplification
    
    # For a more advanced approach, you'd extract skills specifically
    # For now, we'll just return the score
    return round(similarity_score, 2), [] # Placeholder for actual missing skills

def generate_resume_suggestions(resume_text, jd_text):
    """Uses LLM to generate suggestions for tailoring a resume."""
    prompt = f"""
    Analyze the following resume and job description.
    Provide 3-5 specific, actionable bullet points on how to tailor the resume to better match this job description.
    Focus on highlighting relevant skills and experiences.

    ---RESUME---
    {resume_text}

    ---JOB DESCRIPTION---
    {jd_text}
    """
    response = llm.invoke(prompt)
    return response.content

def suggest_skills_to_learn(resume_text, desired_job):
    """Suggests skills for the user to learn for their desired career."""
    prompt = f"""
    Based on this resume and a desired job title of "{desired_job}", what are the top 5 technical skills or tools this person should consider learning to advance their career?
    
    ---RESUME---
    {resume_text}
    """
    response = llm.invoke(prompt)
    return response.content
