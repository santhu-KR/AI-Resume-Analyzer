# 🤖 AI Resume Analyzer

An AI-powered Resume Analyzer built using Python, Flask, Machine Learning and NLP techniques.

The application analyzes a candidate's resume against a job description and provides an ATS-style compatibility score, skill analysis, job-role recommendations and improvement suggestions.

---

## 🚀 Features

- 📄 Upload Resume in PDF or DOCX format
- 🎯 ATS Compatibility Score
- 📊 Resume and Job Description Similarity
- 🧠 Technical Skill Detection
- ✅ Matched Skills
- ⚠️ Missing Skills
- 📋 Resume Quality Score
- 💡 Resume Improvement Suggestions
- 🎯 Recommended Job Roles
- 📜 Analysis History
- 🗄️ SQLite Database
- 🌐 Flask Web Application
- 📱 Responsive Bootstrap UI

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- Bootstrap 5

### Backend

- Python
- Flask

### Machine Learning / NLP

- Scikit-learn
- TF-IDF
- Cosine Similarity

### Resume Processing

- PyPDF2
- python-docx

### Database

- SQLite

---

## 📁 Project Structure

```text
AI-Resume-Analyzer
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates
│   ├── index.html
│   ├── result.html
│   └── history.html
│
├── static
│
├── uploads
│
└── utils
    ├── analyzer.py
    └── resume_parser.py