import sqlite3
import pandas as pd

DB_FILE = "analysis_results.db"

def create_table():
    """Creates the results table in the database if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        resume_name TEXT,
        jd_name TEXT,
        final_score REAL,
        verdict TEXT,
        matching_skills TEXT,
        missing_skills TEXT,
        ai_feedback TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_result(resume_name, jd_name, final_score, verdict, matching, missing, feedback):
    """Saves a single analysis result to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO results (resume_name, jd_name, final_score, verdict, matching_skills, missing_skills, ai_feedback)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (resume_name, jd_name, final_score, verdict, str(matching), str(missing), feedback))
    conn.commit()
    conn.close()

def fetch_all_results():
    """Fetches all results from the database and returns them as a DataFrame."""
    conn = sqlite3.connect(DB_FILE)
    try:
        # Use pandas to read the SQL query directly into a DataFrame
        df = pd.read_sql_query("SELECT * FROM results ORDER BY timestamp DESC", conn)
        return df
    finally:
        conn.close()