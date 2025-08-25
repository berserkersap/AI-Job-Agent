# modules/rag_engine.py
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import config

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=config.GOOGLE_API_KEY)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=config.GOOGLE_API_KEY)

def create_rag_chain(resume_text, job_descriptions):
    """
    Creates a RAG chain from the user's resume and a list of job descriptions.
    """
    # 📚 1. Create the Knowledge Base
    # Combine all text sources into one body of knowledge
    knowledge_base_text = resume_text
    for i, jd in enumerate(job_descriptions):
        knowledge_base_text += f"\n\n--- JOB DESCRIPTION {i+1} ---\n{jd}"

    # ✂️ 2. Chunk the text
    # Split the text into smaller, manageable pieces
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.create_documents([knowledge_base_text])

    # 🔗 3. Create Vector Store (The Retriever)
    # Convert text chunks into vector embeddings and store them
    print("🧠 Building RAG knowledge base from your resume and top jobs...")
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()
    
    # ⛓️ 4. Create the RAG Chain
    # This chain combines the retriever and the LLM
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "Stuff" means it crams all retrieved context into the prompt
        retriever=retriever,
        return_source_documents=True
    )
    
    print("✅ RAG chain created successfully!")
    return rag_chain

def query_rag_chain(rag_chain, job_title):
    """
    Asks a specific question to the RAG chain to get tailored advice.
    """
    query = f"""
    Based on the provided context (my resume and several job descriptions), 
    give me a highly detailed, step-by-step plan to tailor my resume specifically 
    for the role of '{job_title}'. 
    
    Focus on:
    1. A summary statement to add at the top.
    2. Which specific skills from the job descriptions I should emphasize.
    3. How to rephrase bullet points in my experience section to match the job's requirements.
    """
    result = rag_chain({"query": query})
    return result['result']
