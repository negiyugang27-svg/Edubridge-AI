from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

DATABASE = "edutech.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            education TEXT DEFAULT '',
            career TEXT DEFAULT '',
            skills TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =========================================================
# PAGES
# =========================================================

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/login")
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/register")
def register():
    if "user_id" in session:
        return redirect(url_for("home"))

    return render_template("register.html")


# =========================================================
# REGISTER
# =========================================================

@app.route("/api/register", methods=["POST"])
def api_register():

    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    conn = get_db()

    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing:
        conn.close()

        return jsonify({
            "success": False,
            "message": "An account with this email already exists."
        }), 409

    password_hash = hash_password(password)

    cursor = conn.execute("""
        INSERT INTO users
        (name, email, password)
        VALUES (?, ?, ?)
    """, (
        name,
        email,
        password_hash
    ))

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    session["user_id"] = user_id

    return jsonify({
        "success": True,
        "message": "Account created successfully."
    })


# =========================================================
# LOGIN
# =========================================================

@app.route("/api/login", methods=["POST"])
def api_login():

    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Please enter email and password."
        }), 400

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,)).fetchone()

    conn.close()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    if hash_password(password) != user["password"]:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    session["user_id"] = user["id"]

    return jsonify({
        "success": True,
        "message": "Login successful."
    })


# =========================================================
# LOGOUT
# =========================================================

@app.route("/api/logout", methods=["POST"])
def api_logout():

    session.clear()

    return jsonify({
        "success": True
    })


# =========================================================
# CURRENT USER
# =========================================================

@app.route("/api/current-user")
def current_user():

    if "user_id" not in session:
        return jsonify({
            "logged_in": False
        })

    conn = get_db()

    user = conn.execute("""
        SELECT id, name, email, education, career, skills
        FROM users
        WHERE id = ?
    """, (session["user_id"],)).fetchone()

    conn.close()

    if not user:
        session.clear()

        return jsonify({
            "logged_in": False
        })

    skills = []

    if user["skills"]:
        skills = [
            skill.strip()
            for skill in user["skills"].split(",")
            if skill.strip()
        ]

    return jsonify({
        "logged_in": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "education": user["education"],
            "career": user["career"],
            "skills": skills
        }
    })


# =========================================================
# SAVE PROFILE
# =========================================================

@app.route("/api/profile", methods=["POST"])
def save_profile():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json()

    education = data.get("education", "").strip()
    career = data.get("career", "").strip()

    skills = data.get("skills", [])

    if isinstance(skills, list):
        skills_text = ", ".join(skills)
    else:
        skills_text = str(skills)

    conn = get_db()

    conn.execute("""
        UPDATE users
        SET education = ?,
            career = ?,
            skills = ?
        WHERE id = ?
    """, (
        education,
        career,
        skills_text,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Profile saved successfully."
    })


# =========================================================
# SKILL REQUIREMENTS
# =========================================================

CAREER_SKILLS = {

    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Statistics",
        "NumPy",
        "Pandas",
        "TensorFlow"
    ],

    "Data Scientist": [
        "Python",
        "Statistics",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Data Visualization"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "React",
        "Node.js"
    ],

    "Software Developer": [
        "Programming",
        "Data Structures",
        "Algorithms",
        "Git",
        "Problem Solving",
        "Database"
    ],

    "Cybersecurity Analyst": [
        "Networking",
        "Linux",
        "Python",
        "Cybersecurity",
        "Cryptography",
        "Ethical Hacking"
    ],

    "Cloud Engineer": [
        "Linux",
        "Networking",
        "AWS",
        "Docker",
        "Kubernetes",
        "Python"
    ]
}


# =========================================================
# SKILL GAP
# =========================================================

@app.route("/api/skill-gap", methods=["POST"])
def skill_gap():

    data = request.get_json()

    skills = data.get("skills", [])
    career = data.get("career", "")

    required_skills = CAREER_SKILLS.get(
        career,
        []
    )

    normalized_skills = [
        skill.lower().strip()
        for skill in skills
    ]

    matched = []
    missing = []

    for required in required_skills:

        if required.lower() in normalized_skills:
            matched.append(required)
        else:
            missing.append(required)

    if len(required_skills) > 0:

        progress = round(
            len(matched) /
            len(required_skills) *
            100
        )

    else:
        progress = 0

    return jsonify({
        "career": career,
        "required_skills": required_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "progress": progress
    })


# =========================================================
# QUIZ
# =========================================================

@app.route("/api/quiz-result", methods=["POST"])
def quiz_result():

    data = request.get_json()

    answers = data.get("answers", [])

    correct_answers = [
        "python",
        "machine-learning",
        "html",
        "data",
        "algorithm"
    ]

    score = 0

    for i in range(
        min(
            len(answers),
            len(correct_answers)
        )
    ):

        if answers[i].lower() == correct_answers[i]:
            score += 1

    total = len(correct_answers)

    percentage = round(
        score / total * 100
    )

    if percentage >= 80:
        level = "Advanced"

        recommendation = (
            "Excellent performance! "
            "You can start working on advanced "
            "projects and real-world applications."
        )

    elif percentage >= 60:
        level = "Intermediate"

        recommendation = (
            "Good progress! Strengthen your "
            "fundamentals and start building projects."
        )

    else:
        level = "Beginner"

        recommendation = (
            "Focus on your fundamentals first. "
            "Practice regularly and build small projects."
        )

    return jsonify({
        "score": score,
        "total": total,
        "percentage": percentage,
        "level": level,
        "recommendation": recommendation
    })


# =========================================================
# AI TUTOR
# =========================================================

@app.route("/api/tutor", methods=["POST"])
def tutor():

    if "user_id" not in session:
        return jsonify({
            "answer": "Please login first."
        }), 401

    data = request.get_json()

    question = data.get(
        "question",
        ""
    ).strip()

    level = data.get(
        "level",
        "Beginner"
    )

    if not question:
        return jsonify({
            "answer": "Please ask me a question."
        })

    q = question.lower()

    # FREE RULE-BASED AI FALLBACK
    if "python" in q:

        answer = (
            f"In {level} Mode, Python is a "
            "high-level programming language commonly "
            "used in AI, machine learning, automation "
            "and web development. Start by learning "
            "variables, conditions, loops, functions "
            "and data structures."
        )

    elif "machine learning" in q:

        answer = (
            "Machine Learning is a field of AI where "
            "systems learn patterns from data and use "
            "those patterns to make predictions or decisions."
        )

    elif "html" in q:

        answer = (
            "HTML is the structure of a web page. "
            "You can think of HTML as the skeleton, "
            "CSS as the design and JavaScript as the behavior."
        )

    elif "career" in q:

        answer = (
            "A good career path depends on your interests "
            "and current skills. Use the Skill Gap Analysis "
            "in EduTech to compare your skills with a target career."
        )

    elif "skill" in q:

        answer = (
            "Start by identifying your target career, "
            "then compare your current skills with the "
            "skills required for that career. EduTech "
            "can generate a personalized roadmap for you."
        )

    else:

        answer = (
            f"I understand your question. In {level} Mode, "
            "try breaking the topic into smaller concepts. "
            "Start with the basics, practice with examples, "
            "and then move to projects."
        )

    return jsonify({
        "answer": answer
    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )