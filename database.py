import sqlite3
import hashlib


DATABASE_NAME = "data/resume_analyzer.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Resume analysis history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            filename TEXT,
            resume_score INTEGER,
            job_match REAL,
            skills TEXT
        )
    """)

    connection.commit()
    connection.close()


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def register_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, hashed_password)
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


def login_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = ? AND password = ?
        """,
        (username, hashed_password)
    )

    user = cursor.fetchone()

    connection.close()

    return user


def save_analysis(
    username,
    filename,
    resume_score,
    job_match,
    skills
):

    connection = get_connection()
    cursor = connection.cursor()

    skills_string = ", ".join(skills)

    cursor.execute(
        """
        INSERT INTO analysis_history
        (username, filename, resume_score, job_match, skills)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            filename,
            resume_score,
            job_match,
            skills_string
        )
    )

    connection.commit()
    connection.close()


def get_history(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT filename, resume_score, job_match, skills
        FROM analysis_history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    history = cursor.fetchall()

    connection.close()

    return history