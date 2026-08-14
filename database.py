import sqlite3

DATABASE_NAME = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            job_description TEXT NOT NULL,
            score REAL,
            similarity_score REAL,
            skill_score REAL,
            resume_quality TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(
    visitor_id,
    filename,
    job_description,
    score,
    similarity_score,
    skill_score,
    resume_quality,
    matched_skills,
    missing_skills
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analyses (
            visitor_id,
            filename,
            job_description,
            score,
            similarity_score,
            skill_score,
            resume_quality,
            matched_skills,
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        visitor_id,
        filename,
        job_description,
        score,
        similarity_score,
        skill_score,
        resume_quality,
        ", ".join(matched_skills) if isinstance(matched_skills, list) else matched_skills,
        ", ".join(missing_skills) if isinstance(missing_skills, list) else missing_skills
    ))

    connection.commit()
    connection.close()


def get_user_analyses(visitor_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        WHERE visitor_id = ?
        ORDER BY id DESC
    """, (visitor_id,))

    analyses = cursor.fetchall()
    connection.close()

    return analyses