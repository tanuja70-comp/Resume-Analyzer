import streamlit as st

from database import create_tables, register_user, login_user

from analyzer import (
    extract_resume_text,
    find_skills,
    calculate_score,
    generate_suggestions
)


# -----------------------------
# Page settings
# -----------------------------

st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="centered"
)


# Create database tables
create_tables()


# -----------------------------
# Session State
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# -----------------------------
# Login Page
# -----------------------------

def login_page():

    st.title("📄 Smart Resume Analyzer")

    st.write(
        "Analyze your resume and improve your job chances."
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    # Login
    with login_tab:

        st.subheader("Login")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )


    # Register
    with register_tab:

        st.subheader("Create Account")

        username = st.text_input(
            "Username",
            key="register_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button("Register"):

            if password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif not username or not password:

                st.warning(
                    "Please fill all fields."
                )

            else:

                result = register_user(
                    username,
                    password
                )

                if result:

                    st.success(
                        "Account created! Please login."
                    )

                else:

                    st.error(
                        "Username already exists."
                    )


# -----------------------------
# Dashboard
# -----------------------------

def dashboard():

    st.title("📊 Smart Resume Analyzer")

    st.write(
        f"Welcome, **{st.session_state.username}** 👋"
    )

    st.divider()

    # Logout button

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()


    # -----------------------------
    # Resume Upload
    # -----------------------------

    st.header("📄 Upload Your Resume")

    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=["pdf", "docx"]
    )


    if uploaded_file:

        st.success(
            f"File uploaded: {uploaded_file.name}"
        )


        # Analyze button

    if st.button(
    "🔍 Analyze Resume"
):

       resume_text = extract_resume_text(
        uploaded_file
    )

    if resume_text.strip():

        # -----------------------------
        # Find skills
        # -----------------------------

        skills = find_skills(
            resume_text
        )


        # -----------------------------
        # Calculate score
        # -----------------------------

        score = calculate_score(
            resume_text,
            skills
        )


        # -----------------------------
        # Generate suggestions
        # -----------------------------

        suggestions = generate_suggestions(
            resume_text,
            skills
        )


        st.success(
            "Resume analyzed successfully!"
        )


        # -----------------------------
        # Display score
        # -----------------------------

        st.subheader("📊 Resume Score")

        st.metric(
            "Overall Score",
            f"{score}/100"
        )


        # -----------------------------
        # Display skills
        # -----------------------------

        st.subheader(
            "🛠️ Skills Detected"
        )

        if skills:

            for skill in skills:

                st.success(
                    skill.title()
                )

        else:

            st.warning(
                "No skills detected."
            )


        # -----------------------------
        # Suggestions
        # -----------------------------

        st.subheader(
            "💡 Suggestions"
        )

        for suggestion in suggestions:

            st.write(
                "• " + suggestion
            )


        # -----------------------------
        # Resume text
        # -----------------------------

        with st.expander(
            "📃 View Extracted Resume Text"
        ):

            st.text(
                resume_text
            )

    else:

        st.error(
            "Could not extract text from this resume."
        )

        resume_text = extract_resume_text(
                uploaded_file
            )


        if resume_text.strip():

                st.success(
                    "Resume text extracted successfully!"
                )

                st.subheader(
                    "📃 Resume Text"
                )

                st.text_area(
                    "Extracted Content",
                    resume_text,
                    height=400
                )

        else:

                st.error(
                    "Could not extract text from this file."
                )


# -----------------------------
# Main Application
# -----------------------------

if st.session_state.logged_in:

    dashboard()

else:

    login_page()