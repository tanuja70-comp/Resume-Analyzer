import fitz
from docx import Document
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "flask",
    "django",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "machine learning",
    "data science",
    "artificial intelligence",
    "pandas",
    "numpy",
    "scikit-learn",
    "communication",
    "leadership"
]


def extract_pdf_text(file):

    text = ""

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    for page in pdf:

        text += page.get_text()

    return text


def extract_docx_text(file):

    document = Document(file)

    text = []

    for paragraph in document.paragraphs:

        text.append(paragraph.text)

    return "\n".join(text)


def extract_resume_text(file):

    filename = file.name.lower()

    if filename.endswith(".pdf"):

        return extract_pdf_text(file)

    elif filename.endswith(".docx"):

        return extract_docx_text(file)

    return ""


def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills


def calculate_score(text, skills):

    score = 0

    text_lower = text.lower()

    # Skills score
    score += min(
        len(skills) * 4,
        40
    )

    # Resume sections
    sections = [
        "education",
        "experience",
        "projects",
        "skills",
        "certifications"
    ]

    for section in sections:

        if section in text_lower:

            score += 10

    return min(score, 100)


def calculate_job_match(
    resume_text,
    job_description
):

    if not job_description.strip():

        return 0

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


def generate_suggestions(
    text,
    skills
):

    suggestions = []

    text_lower = text.lower()

    if "projects" not in text_lower:

        suggestions.append(
            "Add a Projects section with 2-3 academic projects."
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
            "Your resume contains the main sections. Keep improving your project descriptions."
        )

    return suggestions