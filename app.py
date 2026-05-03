import streamlit as st
import json

EXAM_FILE = "exam.json"
STUDENT_FILE = "students.json"
RESULT_FILE = "results.json"

# ---------------- SESSION STATE ----------------
if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------------- FUNCTIONS ----------------
def create_exam():
    exam = {
        "questions": [
            {"q": "2 + 2 = ?", "options": ["2", "4", "6"], "answer": "4"},
            {"q": "Capital of India?", "options": ["Delhi", "Mumbai", "Chennai"], "answer": "Delhi"}
        ]
    }
    with open(EXAM_FILE, "w") as f:
        json.dump(exam, f)

def register_student(name):
    try:
        with open(STUDENT_FILE, "r") as f:
            students = json.load(f)
    except:
        students = []

    seat = len(students) + 1
    students.append({"name": name, "seat": seat})

    with open(STUDENT_FILE, "w") as f:
        json.dump(students, f)

    return seat

def evaluate(name, answers):
    with open(EXAM_FILE, "r") as f:
        exam = json.load(f)

    score = 0
    for i, q in enumerate(exam["questions"]):
        if answers[i] == q["answer"]:
            score += 1

    try:
        with open(RESULT_FILE, "r") as f:
            results = json.load(f)
    except:
        results = []

    results.append({"name": name, "score": score})

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f)

    return score

# ---------------- UI ----------------

st.title("📘 Smart Examination System")

# Create Exam
if st.button("Create Exam"):
    create_exam()
    st.success("Exam Created!")

# Student Name
name = st.text_input("Enter Student Name")

# Register
if st.button("Register Student"):
    seat = register_student(name)
    st.success(f"{name} got seat {seat}")

# Take Exam
if st.button("Start Exam"):
    with open(EXAM_FILE, "r") as f:
        exam = json.load(f)

    st.session_state.answers = []

    for i, q in enumerate(exam["questions"]):
        ans = st.selectbox(q["q"], q["options"], key=i)
        st.session_state.answers.append(ans)

# Submit
if st.button("Submit Exam"):
    if name and st.session_state.answers:
        score = evaluate(name, st.session_state.answers)
        st.success(f"Score: {score}")
    else:
        st.warning("Please enter name and complete exam")

# Show Results
if st.button("Show Results"):
    try:
        with open(RESULT_FILE, "r") as f:
            results = json.load(f)

        st.write("📊 Results:")
        for r in results:
            st.write(f"{r['name']} → {r['score']}")
    except:
        st.warning("No results yet")
