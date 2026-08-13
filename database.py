import sqlite3


DATABASE_NAME = "database.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            resume_filename TEXT NOT NULL,

            job_description TEXT NOT NULL,

            ats_score REAL,

            similarity_score REAL,

            skill_score REAL,

            resume_quality REAL,

            matched_skills TEXT,

            missing_skills TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


def save_analysis(
    resume_filename,
    job_description,
    ats_score,
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

            resume_filename,
            job_description,
            ats_score,
            similarity_score,
            skill_score,
            resume_quality,
            matched_skills,
            missing_skills

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        resume_filename,

        job_description,

        ats_score,

        similarity_score,

        skill_score,

        resume_quality,

        ", ".join(matched_skills),

        ", ".join(missing_skills)

    ))

    connection.commit()

    connection.close()


def get_all_analyses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        ORDER BY created_at DESC
    """)

    analyses = cursor.fetchall()

    connection.close()

    return analyses


# Create database table
# when this file is used.

create_table()