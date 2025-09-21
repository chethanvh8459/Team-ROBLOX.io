import streamlit as st
import os
import pandas as pd
from parser import extract_text
from analyzer import standardize_text, extract_skills
from scorer import calculate_relevance_score, calculate_semantic_similarity, get_verdict
from feedback import generate_feedback
import database as db


# --- FIX 1: Define the helper function here in app.py ---
def save_uploaded_file(uploaded_file, directory):
    """Saves an uploaded file to a specified directory."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# --- Page Configuration ---
st.set_page_config(page_title="Resume Relevance Checker", layout="wide", page_icon="📄")

# --- Initialize Database ---
db.create_table()

# --- Sidebar ---
with st.sidebar:
    st.image("Icon.png", width=200)
    st.header("Configuration")
    google_api_key = st.text_input("Enter Your Google AI API Key", type="password", help="Your API key is not stored.")
    
    st.divider()
    
    st.header("Navigation")
    page = st.radio("Go to", ["Analyzer", "Dashboard"], label_visibility="hidden")

# --- Page Routing ---
if page == "Analyzer":
    st.title("📄 Automated Resume Relevance Analyzer")
    st.caption("Upload a job description and a resume to see the magic happen.")

    JD_DIR = "uploads/jds"
    RESUME_DIR = "uploads/resumes"

    col1, col2 = st.columns(2)
    with col1:
        job_description = st.file_uploader("1. Upload Job Description", type=['pdf', 'docx'])
    with col2:
        resume = st.file_uploader("2. Upload Your Resume", type=['pdf', 'docx'])

    if st.button("✨ Analyze Relevance", use_container_width=True):
        if not google_api_key:
            st.error("Please enter your Google AI API Key in the sidebar.")
        elif job_description is not None and resume is not None:
            with st.spinner('Performing deep analysis... This might take a moment.'):
                # --- FIX 2: Call the local function without 'db.' ---
                jd_path = save_uploaded_file(job_description, JD_DIR)
                resume_path = save_uploaded_file(resume, RESUME_DIR)
                
                jd_text = extract_text(jd_path)
                resume_text = extract_text(resume_path)
                jd_cleaned = standardize_text(jd_text)
                resume_cleaned = standardize_text(resume_text)
                jd_skills = extract_skills(jd_cleaned)
                resume_skills = extract_skills(resume_cleaned)
                hard_match_score, matching_skills, missing_skills = calculate_relevance_score(jd_skills, resume_skills)
                semantic_score = calculate_semantic_similarity(jd_text, resume_text)
                final_score = (0.6 * hard_match_score) + (0.4 * semantic_score)
                verdict, verdict_reason = get_verdict(final_score)
                ai_feedback = generate_feedback(google_api_key, jd_text, resume_text, missing_skills)
                db.save_result(resume.name, job_description.name, final_score, verdict, matching_skills, missing_skills, ai_feedback)
            
            st.success("Analysis Complete!")
            st.header("Relevance Analysis Report")
            
            st.subheader(f"Verdict: {verdict}")
            st.info(verdict_reason)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(label="Final Weighted Score", value=f"{final_score:.2f}%")
            with c2:
                st.metric(label="Keyword Match", value=f"{hard_match_score:.2f}%")
            with c3:
                st.metric(label="Semantic Similarity", value=f"{semantic_score:.2f}%")

            st.progress(int(final_score))
            
            st.subheader("Skill Analysis")
            st.markdown(f"**✅ Skills Matched:** `{'`, `'.join(matching_skills) if matching_skills else 'None'}`")
            st.markdown(f"**❌ Skills Missing:** `{'`, `'.join(missing_skills) if missing_skills else 'None'}`")

            st.subheader("🤖 AI-Powered Feedback")
            st.markdown(ai_feedback)
        else:
            st.error("Please upload both a Job Description and a Resume.")

elif page == "Dashboard":
    st.title("📊 Analysis Results Dashboard")
    st.caption("Review all past analysis reports.")
    
    results_df = db.fetch_all_results()
    
    if results_df.empty:
        st.warning("No analysis results found. Please run an analysis on the 'Analyzer' page first.")
    else:
        st.dataframe(results_df, use_container_width=True)
        
        st.subheader("Full Report Details")
        selected_id = st.selectbox("Select a report to view its full details", results_df['id'])
        if selected_id:
            report = results_df[results_df['id'] == selected_id].iloc[0]
            with st.container(border=True):
                st.write(f"**Resume:** {report['resume_name']} | **Job Description:** {report['jd_name']}")
                st.divider()
                st.write(f"**Verdict:** {report['verdict']} ({report['final_score']:.2f}%)")
                st.write("**AI Feedback:**")
                st.info(report['ai_feedback'])