import streamlit as st
import pandas as pd

# 🎬 Show animated logo
st.image("assets/logo.gif", width=200)
st.title("Smart SGPA & CGPA Calculator - Anurag University")

# 📌 Grade points based on Anurag University system
grade_mapping = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "F": 0
}

# Get grade list
grade_options = list(grade_mapping.keys())

# Main function
mode = st.selectbox("Choose Mode", ["SGPA", "CGPA"])

if mode == "SGPA":
    num_subjects = st.number_input("Enter number of subjects", min_value=1, step=1)
    data = []

    for i in range(int(num_subjects)):
        st.subheader(f"Subject {i + 1}")
        credit = st.number_input(f"Credits for Subject {i + 1}", min_value=1, step=1, key=f"credit_{i}")
        grade = st.selectbox(f"Grade for Subject {i + 1}", grade_options, key=f"grade_{i}")
        data.append({"Subject": f"Subject {i+1}", "Credits": credit, "Grade": grade})

    df = pd.DataFrame(data)
    df["Grade Point"] = df["Grade"].map(grade_mapping)
    df["Result"] = df["Grade"].apply(lambda x: "P" if x != "F" else "**:red[F]**")
    df["Credit x Grade"] = df["Credits"] * df["Grade Point"]

    if not df.empty:
        st.subheader("Subject-wise Grades")
        st.dataframe(df[["Subject", "Credits", "Grade", "Result"]], use_container_width=True)

        total_credits = df["Credits"].sum()
        total_score = df["Credit x Grade"].sum()

        if total_credits > 0:
            sgpa = total_score / total_credits
            st.success(f"📊 SGPA: **{sgpa:.2f}**")
        else:
            st.warning("Please enter valid credit values.")

elif mode == "CGPA":
    num_sems = st.number_input("Enter number of semesters", min_value=1, step=1)
    all_sem_data = []
    cgpa_total_credits = 0
    cgpa_total_points = 0

    for sem in range(int(num_sems)):
        st.header(f"Semester {sem + 1}")
        sub_count = st.number_input(f"Number of subjects in Semester {sem + 1}", min_value=1, step=1, key=f"subcount_{sem}")
        sem_data = []
        sem_credits = 0
        sem_score = 0

        for sub in range(int(sub_count)):
            credit = st.number_input(f"Credits for Subject {sub+1} (Sem {sem+1})", min_value=1, step=1, key=f"sem{sem}_sub{sub}_credit")
            grade = st.selectbox(f"Grade for Subject {sub+1} (Sem {sem+1})", grade_options, key=f"sem{sem}_sub{sub}_grade")
            point = grade_mapping[grade]
            sem_data.append((credit, grade))
            sem_credits += credit
            sem_score += credit * point

        if sem_credits > 0:
            sem_sgpa = sem_score / sem_credits
            st.success(f"✅ SGPA of Semester {sem + 1}: **{sem_sgpa:.2f}**")
            cgpa_total_credits += sem_credits
            cgpa_total_points += sem_score
        else:
            st.warning(f"Invalid credits in Semester {sem+1}")

    if cgpa_total_credits > 0:
        cgpa = cgpa_total_points / cgpa_total_credits
        st.balloons()
        st.success(f"🎓 **Overall CGPA: {cgpa:.2f}**")
