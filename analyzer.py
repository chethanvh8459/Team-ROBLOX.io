import spacy
import re
from spacy.matcher import Matcher

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def standardize_text(text):
    """
    Cleans and standardizes the input text by converting to lowercase,
    removing extra whitespace and newlines.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
    text = text.strip()  # Remove leading/trailing whitespace
    return text

def extract_skills(text):
    """
    Extracts skills from the text using a predefined skill list and spaCy's Matcher.
    """
    # Predefined list of skills (can be expanded)
    SKILL_LIST = [
        "python", "java", "c++", "sql", "mysql", "postgresql",
        "machine learning", "data analysis", "data science",
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
        "react", "angular", "vue", "javascript", "html", "css",
        "flask", "django", "fastapi", "aws", "azure", "gcp"
    ]
    
    matcher = Matcher(nlp.vocab)
    
    # Create patterns for each skill
    for skill in SKILL_LIST:
        pattern = [{"LOWER": part} for part in skill.split()]
        matcher.add(skill.upper(), [pattern])
        
    doc = nlp(text)
    matches = matcher(doc)
    
    found_skills = set()
    for match_id, start, end in matches:
        skill_name = nlp.vocab.strings[match_id]
        found_skills.add(skill_name.lower())
        
    return list(found_skills)