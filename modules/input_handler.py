# modules/input_handler.py
import PyPDF2
import docx

def parse_resume(file_path):
    """Parses a resume file (PDF or DOCX) and returns its text content."""
    text = ""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        print(f"Unsupported file format: {file_path}")
        return None
    return text
