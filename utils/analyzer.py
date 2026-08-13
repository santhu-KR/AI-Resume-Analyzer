import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# TECHNICAL SKILLS
# ==========================================

SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "express",
    "flask",
    "django",
    "spring boot",
    "mysql",
    "mongodb",
    "sql",
    "git",
    "github",
    "docker",
    "aws",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "scikit-learn",
    "data science",
    "data analysis",
    "rest api",
    "api",
    "bootstrap"
]


# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# EXTRACT SKILLS
# ==========================================

def extract_skills(text):

    text = clean_text(text)

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:

            found_skills.append(skill)

    return sorted(
        set(found_skills)
    )


# ==========================================
# CALCULATE RESUME/JOB SIMILARITY
# ==========================================

def calculate_similarity(
    resume_text,
    job_description
):

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


# ==========================================
# RESUME QUALITY SCORE
# ==========================================

def calculate_resume_quality(text):

    score = 0

    text_lower = text.lower()

    # Email
    if re.search(
        r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        text
    ):

        score += 10


    # Phone number
    digits = re.sub(
        r"\D",
        "",
        text
    )

    if len(digits) >= 10:

        score += 10


    # Education
    if any(
        word in text_lower
        for word in [
            "education",
            "degree",
            "bachelor",
            "master",
            "mca",
            "bca",
            "btech"
        ]
    ):

        score += 15


    # Skills section
    if "skills" in text_lower:

        score += 15


    # Projects section
    if "project" in text_lower:

        score += 15


    # Experience
    if any(
        word in text_lower
        for word in [
            "experience",
            "internship",
            "work experience"
        ]
    ):

        score += 15


    # Certifications
    if any(
        word in text_lower
        for word in [
            "certification",
            "certificate",
            "certifications"
        ]
    ):

        score += 10


    # Achievements
    if any(
        word in text_lower
        for word in [
            "achievement",
            "award",
            "accomplishment"
        ]
    ):

        score += 10


    return min(
        score,
        100
    )


# ==========================================
# SUGGESTIONS
# ==========================================

def generate_suggestions(
    resume_text,
    job_description,
    missing_skills,
    resume_quality
):

    suggestions = []

    text = resume_text.lower()


    # Missing skills
    if missing_skills:

        suggestions.append(
            "Add relevant missing skills only if you genuinely have experience with them."
        )


    # Skills section
    if "skills" not in text:

        suggestions.append(
            "Add a dedicated Technical Skills section."
        )


    # Projects
    if "project" not in text:

        suggestions.append(
            "Add a Projects section with technologies and measurable results."
        )


    # Experience
    if (
        "experience" not in text
        and
        "internship" not in text
    ):

        suggestions.append(
            "Add relevant internship, work experience, or practical project experience."
        )


    # Education
    if "education" not in text:

        suggestions.append(
            "Add a clear Education section."
        )


    # Achievements
    if (
        "achievement" not in text
        and
        "award" not in text
    ):

        suggestions.append(
            "Add measurable achievements where possible."
        )


    # Overall quality
    if resume_quality < 60:

        suggestions.append(
            "Improve the overall structure and completeness of your resume."
        )


    if not suggestions:

        suggestions.append(
            "Your resume has good structure and job alignment."
        )


    return suggestions


# ==========================================
# JOB ROLE RECOMMENDATION
# ==========================================

def recommend_roles(resume_skills):

    roles = {

        "Python Developer": [
            "python",
            "flask",
            "django",
            "pandas",
            "numpy"
        ],

        "Web Developer": [
            "html",
            "css",
            "javascript",
            "bootstrap",
            "react"
        ],

        "Java Developer": [
            "java",
            "spring boot",
            "mysql",
            "sql"
        ],

        "Data Analyst": [
            "python",
            "pandas",
            "numpy",
            "sql",
            "data analysis"
        ],

        "Machine Learning Engineer": [
            "python",
            "machine learning",
            "numpy",
            "pandas",
            "scikit-learn",
            "tensorflow"
        ],

        "Backend Developer": [
            "python",
            "java",
            "node.js",
            "express",
            "flask",
            "sql",
            "mongodb"
        ]
    }


    recommendations = []


    for role, required_skills in roles.items():

        matched = (
            set(resume_skills)
            &
            set(required_skills)
        )


        if matched:

            score = (
                len(matched)
                /
                len(required_skills)
            ) * 100


            recommendations.append({

                "role": role,

                "score": round(
                    score,
                    2
                ),

                "skills": sorted(
                    matched
                )

            })


    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return recommendations[:3]


# ==========================================
# MAIN RESUME ANALYSIS
# ==========================================

def analyze_resume(
    resume_text,
    job_description
):

    original_resume_text = resume_text


    # Clean text
    resume_text = clean_text(
        resume_text
    )

    job_description = clean_text(
        job_description
    )


    # ======================================
    # Extract skills
    # ======================================

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )


    # ======================================
    # Matched skills
    # ======================================

    matched_skills = list(
        set(resume_skills)
        &
        set(job_skills)
    )


    # ======================================
    # Missing skills
    # ======================================

    missing_skills = list(
        set(job_skills)
        -
        set(resume_skills)
    )


    # ======================================
    # Skill score
    # ======================================

    if len(job_skills) > 0:

        skill_score = (
            len(matched_skills)
            /
            len(job_skills)
        ) * 100

    else:

        skill_score = 0


    # ======================================
    # Similarity score
    # ======================================

    if (
        resume_text
        and
        job_description
    ):

        similarity_score = calculate_similarity(
            resume_text,
            job_description
        )

    else:

        similarity_score = 0


    # ======================================
    # Resume quality
    # ======================================

    resume_quality = calculate_resume_quality(
        original_resume_text
    )


    # ======================================
    # Final ATS score
    #
    # Skill Match    = 50%
    # Similarity     = 30%
    # Resume Quality = 20%
    # ======================================

    final_score = (

        skill_score * 0.50

        +

        similarity_score * 0.30

        +

        resume_quality * 0.20

    )


    final_score = round(
        final_score,
        2
    )


    # ======================================
    # Suggestions
    # ======================================

    suggestions = generate_suggestions(

        original_resume_text,

        job_description,

        missing_skills,

        resume_quality

    )


    # ======================================
    # Job role recommendations
    # ======================================

    role_recommendations = recommend_roles(

        resume_skills

    )


    # ======================================
    # Return all results
    # ======================================

    return {

        "score": final_score,

        "similarity_score": similarity_score,

        "skill_score": round(
            skill_score,
            2
        ),

        "resume_quality": round(
            resume_quality,
            2
        ),

        "resume_skills": resume_skills,

        "job_skills": job_skills,

        "matched_skills": sorted(
            matched_skills
        ),

        "missing_skills": sorted(
            missing_skills
        ),

        "suggestions": suggestions,

        "role_recommendations": role_recommendations

    }