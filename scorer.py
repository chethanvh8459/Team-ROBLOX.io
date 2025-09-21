from sentence_transformers import SentenceTransformer, util

# Load a pre-trained model. This will be downloaded automatically the first time.
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_relevance_score(jd_skills, resume_skills):
    """
    Calculates a "hard match" score based on skill overlap.
    """
    if not jd_skills:
        return 0, [], []

    jd_skills_set = set(jd_skills)
    resume_skills_set = set(resume_skills)

    matching_skills = list(jd_skills_set.intersection(resume_skills_set))
    missing_skills = list(jd_skills_set.difference(resume_skills_set))

    score = (len(matching_skills) / len(jd_skills_set)) * 100
    return score, matching_skills, missing_skills

def calculate_semantic_similarity(jd_text, resume_text):
    """
    Calculates semantic similarity using sentence embeddings.
    """
    # Encode the texts into embeddings (vectors)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # Calculate cosine similarity
    cosine_scores = util.cos_sim(jd_embedding, resume_embedding)

    # Convert the score to a 0-100 scale
    similarity_score = (cosine_scores.item() * 100)
    # Ensure the score is not negative
    return max(0, similarity_score)

def get_verdict(score):
    """
    Provides a qualitative verdict based on a numerical score.
    """
    if score >= 75:
        return "High Suitability", "This resume is a strong match for the job description."
    elif score >= 50:
        return "Medium Suitability", "This resume shows potential but has some gaps."
    else:
        return "Low Suitability", "This resume has significant gaps with the job description."