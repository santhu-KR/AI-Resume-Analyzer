from flask import Flask, render_template, request

from werkzeug.utils import secure_filename

import os


# ==========================================
# PROJECT MODULES
# ==========================================

from utils.resume_parser import extract_resume_text

from utils.analyzer import analyze_resume

from database import (
    save_analysis,
    get_all_analyses,
    create_table
)


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# UPLOAD CONFIGURATION
# ==========================================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}

app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER


# Create uploads folder
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# Create database table
create_table()


# ==========================================
# CHECK FILE EXTENSION
# ==========================================

def allowed_file(filename):

    return (
        "."
        in filename

        and

        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# ANALYZE RESUME
# ==========================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # -----------------------------
    # Check resume
    # -----------------------------

    if "resume" not in request.files:

        return "Resume file is required"


    resume = request.files[
        "resume"
    ]


    # -----------------------------
    # Get job description
    # -----------------------------

    job_description = request.form.get(
        "job_description",
        ""
    )


    # -----------------------------
    # Validate filename
    # -----------------------------

    if resume.filename == "":

        return "Please select a resume"


    # -----------------------------
    # Validate file type
    # -----------------------------

    if not allowed_file(
        resume.filename
    ):

        return (
            "Only PDF and DOCX files are supported"
        )


    # -----------------------------
    # Validate job description
    # -----------------------------

    if not job_description.strip():

        return (
            "Please enter a job description"
        )


    # -----------------------------
    # Secure filename
    # -----------------------------

    filename = secure_filename(
        resume.filename
    )


    # -----------------------------
    # File path
    # -----------------------------

    file_path = os.path.join(

        app.config[
            "UPLOAD_FOLDER"
        ],

        filename

    )


    # -----------------------------
    # Save resume
    # -----------------------------

    resume.save(
        file_path
    )


    try:

        # =========================
        # Extract resume text
        # =========================

        resume_text = extract_resume_text(
            file_path
        )


        if not resume_text.strip():

            return (
                "Could not extract text from the resume"
            )


        # =========================
        # Analyze resume
        # =========================

        result = analyze_resume(

            resume_text,

            job_description

        )


        # =========================
        # Save analysis to database
        # =========================

        save_analysis(

            filename,

            job_description,

            result["score"],

            result[
                "similarity_score"
            ],

            result[
                "skill_score"
            ],

            result[
                "resume_quality"
            ],

            result[
                "matched_skills"
            ],

            result[
                "missing_skills"
            ]

        )


        # =========================
        # Show result page
        # =========================

        return render_template(

            "result.html",

            result=result

        )


    except Exception as error:

        return (
            f"Error analyzing resume: {error}"
        )


# ==========================================
# ANALYSIS HISTORY
# ==========================================

@app.route("/history")
def history():

    analyses = get_all_analyses()

    return render_template(

        "history.html",

        analyses=analyses

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )