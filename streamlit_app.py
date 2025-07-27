import streamlit as st
from PIL import Image

st.set_page_config(page_title="Smart GPA App", layout="centered")
# Display animated logo
st.image("assets/logo.gif", width=200)

st.title("🎓 Smart GPA Calculator (Anurag University)")
mode = st.sidebar.radio("Select Mode", ("SGPA", "CGPA"))

# Grade to point mapping
grade_point_map = {
    "O": 10, "A+": 9, "A": 8, "B+": 7,
    "B": 6, "C": 5, "F": 0
}

grade_options = list(grade_point_map.keys())

def calculate_sgpa(grades, credits):
    total_points = sum(grade_point_map[g] * c for g, c in zip(grades, credits))
    total_credits = sum(credits)
    return round(total_points / total_credits, 2) if total_credits else 0.0

def calculate_cgpa(all_sgpas, all_credits):
    total_weighted_sgpa = sum(sgpa * credit for sgpa, credit in zip(all_sgpas, all_credits))
    total_credits = sum(all_credits)
    return round(total_weighted_sgpa / total_credits, 2) if total_credits else 0.0

if mode == "SGPA":
    st.header("📘 SGPA Calculator")
    num_subjects = st.number_input("Enter number of subjects", min_value=1, step=1)

    grades, credits = [], []
    for i in range(int(num_subjects)):
        col1, col2 = st.columns(2)
        with col1:
            grade = st.selectbox(f"Subject {i+1} Grade", grade_options, key=f"g{i}")
        with col2:
            credit = st.number_input(f"Subject {i+1} Credits", min_value=1, step=1, key=f"c{i}")
        grades.append(grade)
        credits.append(credit)

    if st.button("Calculate SGPA"):
        sgpa = calculate_sgpa(grades, credits)
        st.success(f"🎯 Your SGPA is: {sgpa}")
        st.markdown("### 📄 Subject Details")
        for i in range(int(num_subjects)):
            status = "P" if grades[i] != "F" else "F"
            color = "red" if status == "F" else "green"
            st.markdown(f"- Subject {i+1}: Grade = **{grades[i]}**, Credits = **{credits[i]}**, "
                        f"Status = <span style='color:{color}'><strong>{status}</strong></span>", unsafe_allow_html=True)

elif mode == "CGPA":
    st.header("📗 CGPA Calculator")
    num_semesters = st.number_input("Enter number of semesters", min_value=1, step=1)

    all_sgpas, all_credits = [], []
    for i in range(int(num_semesters)):
        col1, col2 = st.columns(2)
        with col1:
            sgpa = st.number_input(f"Semester {i+1} SGPA", min_value=0.0, max_value=10.0, step=0.01, key=f"sgpa{i}")
        with col2:
            credit = st.number_input(f"Semester {i+1} Total Credits", min_value=1, step=1, key=f"credit{i}")
        all_sgpas.append(sgpa)
        all_credits.append(credit)import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Smart GPA App", layout="centered")

# --- LOGO ---
st.image("assets/logo.gif", width=200)

# --- TITLE ---
st.title("🎓 Smart GPA & CGPA Calculator")
st.markdown("Calculate your SGPA and CGPA easily following **Anurag University** guidelines.")

# --- MODE SELECTOR ---
mode = st.radio("Choose Mode", ["SGPA Calculator", "CGPA Calculator"])

grade_map = {
    "O": 10, "S": 9, "A": 8, "B": 7, "C": 6, "D": 5, "F": 0
}
grade_list = list(grade_map.keys())

def display_grades_table(df):
    df['Grade Point'] = df['Grade'].map(grade_map)
    df['Status'] = df['Grade'].apply(lambda x: 'F' if x == 'F' else 'P')
    df['Status'] = df['Status'].apply(lambda x: f":red[{x}]" if x == 'F' else f":green[{x}]")
    return df

if mode == "SGPA Calculator":
    st.header("📘 SGPA Calculator")

    num_subjects = st.number_input("Enter number of subjects", min_value=1, step=1)
    
    if num_subjects:
        subject_data = []
        for i in range(num_subjects):
            st.subheader(f"Subject {i+1}")
            name = st.text_input(f"Subject Name {i+1}", key=f"name{i}")
            credits = st.number_input(f"Credits for {name or f'Subject {i+1}'}", min_value=1, step=1, key=f"credit{i}")
            grade = st.selectbox(f"Grade for {name or f'Subject {i+1}'}", grade_list, key=f"grade{i}")
            subject_data.append({"Subject": name, "Credits": credits, "Grade": grade})

        if st.button("Calculate SGPA"):
            df = pd.DataFrame(subject_data)
            df = display_grades_table(df)
            st.dataframe(df, use_container_width=True)

            total_credits = df['Credits'].sum()
            total_points = sum(df['Credits'] * df['Grade Point'])
            sgpa = round(total_points / total_credits, 2)

            st.success(f"🎯 Your SGPA is: **{sgpa}**")

elif mode == "CGPA Calculator":
    st.header("📗 CGPA Calculator")

    num_semesters = st.number_input("Enter number of semesters", min_value=1, step=1)

    if num_semesters:
        semester_data = []
        for i in range(num_semesters):
            st.subheader(f"Semester {i+1}")
            sem_credits = st.number_input(f"Total Credits in Semester {i+1}", min_value=1, step=1, key=f"sem_credit{i}")
            sem_sgpa = st.number_input(f"SGPA in Semester {i+1}", min_value=0.0, max_value=10.0, step=0.01, key=f"sem_sgpa{i}")
            semester_data.append({"Semester": i+1, "Credits": sem_credits, "SGPA": sem_sgpa})

        if st.button("Calculate CGPA"):
            df = pd.DataFrame(semester_data)
            st.dataframe(df, use_container_width=True)

            total_credits = df['Credits'].sum()
            total_weighted_sgpa = sum(df['Credits'] * df['SGPA'])
            cgpa = round(total_weighted_sgpa / total_credits, 2)

            st.success(f"🎓 Your CGPA is: **{cgpa}**")

# --- FOOTER ---
st.markdown("---")
st.caption("Made with by P Avinash • Powered by Streamlit")


    if st.button("Calculate CGPA"):
        cgpa = calculate_cgpa(all_sgpas, all_credits)
        st.success(f"📊 Your CGPA is: {cgpa}")
