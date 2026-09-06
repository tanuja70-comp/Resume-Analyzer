import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Skills database
# -----------------------------

SKILLS = [
    "python", "java", "c", "c++", "javascript",
    "html", "css", "react", "node.js",
    "flask", "django", "sql", "mysql",
    "mongodb", "git", "github",
    "machine learning", "data science",
    "artificial intelligence", "pandas",
    "numpy", "scikit-learn",
    "communication", "leadership"
]

# -----------------------------
# Extract text from PDF
# -----------------------------

def extract_pdf_text(file):
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


# -----------------------------
# Extract text from DOCX
# -----------------------------

def extract_docx_text(file):
    document = Document(file)

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    return "\n".join(text)


# -----------------------------
# Detect skills
# -----------------------------

def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# -----------------------------
# Resume score
# -----------------------------

def calculate_score(text, skills):

    score = 0

    # Skills
    score += min(len(skills) * 4, 40)

    # Resume sections
    sections = [
        "education",
        "experience",
        "projects",
        "skills",
        "certifications"
    ]

    for section in sections:
        if section in text.lower():
            score += 10

    return min(score, 100)


# -----------------------------
# Job matching
# -----------------------------

def calculate_job_match(resume_text, job_description):

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)


# -----------------------------
# Suggestions
# -----------------------------

def generate_suggestions(text, skills):

    suggestions = []

    text_lower = text.lower()

    if "projects" not in text_lower:
        suggestions.append(
            "Add a Projects section with 2–3 academic projects."
        )

    if "experience" not in text_lower:
        suggestions.append(
            "Add internship, training, or practical experience if available."
        )

    if "certifications" not in text_lower:
        suggestions.append(
            "Add relevant certifications or courses."
        )

    if len(skills) < 5:
        suggestions.append(
            "Mention more relevant technical skills."
        )

    if "github" not in text_lower:
        suggestions.append(
            "Consider adding your GitHub profile."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has the main sections. Keep improving project descriptions."
        )

    return suggestions


# -----------------------------
# Application UI
# -----------------------------

st.title("📄 Smart Resume Analyzer")

st.write(
    "Upload your resume and analyze its skills, score, and job compatibility."
)

st.divider()

# Upload resume

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"]
)

# Job description

job_description = st.text_area(
    "Paste Job Description (Optional)",
    height=200,
    placeholder="Paste the job description here..."
)


if uploaded_file:

    # -------------------------
    # Extract resume text
    # -------------------------

    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_pdf_text(uploaded_file)

    else:
        resume_text = extract_docx_text(uploaded_file)

    if not resume_text.strip():

        st.error("Could not extract text from the resume.")

    else:

        # -------------------------
        # Analyze
        # -------------------------

        skills = find_skills(resume_text)

        score = calculate_score(
            resume_text,
            skills
        )

        suggestions = generate_suggestions(
            resume_text,
            skills
        )

        # -------------------------
        # Display score
        # -------------------------

        st.subheader("📊 Resume Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Resume Score",
                f"{score}/100"
            )

        with col2:
            st.metric(
                "Skills Found",
                len(skills)
            )

        with col3:

            if job_description.strip():

                match = calculate_job_match(
                    resume_text,
                    job_description
                )

                st.metric(
                    "Job Match",
                    f"{match}%"
                )

            else:

                st.metric(
                    "Job Match",
                    "N/A"
                )

        st.divider()

        # -------------------------
        # Skills
        # -------------------------

        st.subheader("🛠️ Skills Detected")

        if skills:

            for skill in skills:
                st.success(skill.title())

        else:

            st.warning(
                "No skills were detected."
            )

        # -------------------------
        # Suggestions
        # -------------------------

        st.subheader("💡 Suggestions")

        for suggestion in suggestions:

            st.write(
                "• " + suggestion
            )

        # -------------------------
        # Resume text
        # -------------------------

        with st.expander("📃 View Extracted Resume Text"):

            st.text(resume_text)