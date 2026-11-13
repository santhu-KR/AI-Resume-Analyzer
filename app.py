from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import os
import uuid

from utils.resume_parser import extract_resume_text
from utils.analyzer import analyze_resume
from database import save_analysis, get_user_analyses, create_table


app = Flask(__name__)

# Set SECRET_KEY in Render Environment Variables.
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
create_table()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_visitor_id():
    if "visitor_id" not in session:
        session["visitor_id"] = str(uuid.uuid4())

    return session["visitor_id"]


@app.route("/")
def home():
    get_visitor_id()
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    visitor_id = get_visitor_id()

    if "resume" not in request.files:
        return "Resume file is required"

    resume = request.files["resume"]
    job_description = request.form.get("job_description", "")

    if resume.filename == "":
        return "Please select a resume"

    if not allowed_file(resume.filename):
        return "Only PDF and DOCX files are supported"

    if not job_description.strip():
        return "Please enter a job description"

    original_filename = secure_filename(resume.filename)

    # Prevent one visitor's file from overwriting another visitor's file.
    filename = f"{uuid.uuid4()}_{original_filename}"
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    resume.save(file_path)

    try:
        resume_text = extract_resume_text(file_path)

        if not resume_text.strip():
            return "Could not extract text from the resume"

        result = analyze_resume(resume_text, job_description)

        save_analysis(
            visitor_id,
            original_filename,
            job_description,
            result["score"],
            result["similarity_score"],
            result["skill_score"],
            result["resume_quality"],
            result["matched_skills"],
            result["missing_skills"]
        )

        return render_template("result.html", result=result)

    except Exception as error:
        return f"Error analyzing resume: {error}"


@app.route("/history")
def history():
    visitor_id = get_visitor_id()

    # Shows only analyses from this browser/user.
    analyses = get_user_analyses(visitor_id)

    return render_template("history.html", analyses=analyses)


if __name__ == "__main__":
     app.run(host='127.0.0.1', port=5000, debug=False)
        app.run(debug=True)
