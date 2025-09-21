import google.generativeai as genai

def generate_feedback(api_key, jd_text, resume_text, missing_skills):
    """
    Generates personalized feedback using the Gemini model.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Create a detailed prompt for the model
        prompt = f"""
        As an expert career coach, provide personalized feedback for a student based on their resume and a specific job description.
        The student is missing the following key skills required for the job: {', '.join(missing_skills)}.

        Here is the Job Description:
        ---
        {jd_text}
        ---

        Here is the Student's Resume:
        ---
        {resume_text}
        ---

        Provide constructive feedback in 3-4 concise bullet points. Focus on how the student can better highlight their existing experience or what specific projects or skills they should focus on acquiring to bridge the gap for this role.
        Address the student directly in a positive and encouraging tone.
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating feedback: Could not connect to the generative AI service. Please check your API key and configuration. Details: {e}"