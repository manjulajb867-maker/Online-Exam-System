import streamlit as st
import json
import os

EXAM_FILE = "exam.json"
STUDENT_FILE = "students.json"
RESULT_FILE = "results.json"

# Create Exam
def create_exam():
    exam = {
        "questions": [
            {"q": "2 + 2 = ?", "options": ["2", "4", "6"], "answer": "4"},
            {"q": "Capital of India?", "options": ["Delhi", "Mumbai", "Chennai"], "answer": "Delhi"}
        ]
    }
    with open(EXAM_FILE, "w") as f:
        json.dump(exam, f)

# Register Student
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

# Evaluate
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

if st.button("Create Exam"):
    create_exam()
    st.success("Exam Created!")

name = st.text_input("Enter Student Name")

if st.button("Register Student"):
    seat = register_student(name)
    st.success(f"{name} got seat {seat}")

if st.button("Take Exam"):
    with open(EXAM_FILE, "r") as f:
        exam = json.load(f)

    answers = []
    for q in exam["questions"]:
        ans = st.selectbox(q["q"], q["options"])
        answers.append(ans)

    if st.button("Submit Exam"):
        score = evaluate(name, answers)
        st.success(f"Score: {score}")

if st.button("Show Results"):
    try:
        with open(RESULT_FILE, "r") as f:
            results = json.load(f)
        st.write(results)
    except:
        st.warning("No results yet")
