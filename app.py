import streamlit as st
import requests

st.title("AI Interview Question Generator")

role = st.selectbox(
    "Select Job Role",
    ["ML Engineer","Data Scientist","Backend","HR"]
)

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Generate Questions"):

    if resume is None:
        st.error("Please upload resume")
    else:
        files = {"file": resume.getvalue()}
        data = {"role": role}

        with st.spinner("Analyzing Resume..."):
            r = requests.post(
                "http://localhost:8000/upload_resume/",
                files={"file": resume},
                data=data
            )

        if r.status_code == 200:
            res = r.json()

            
            st.subheader("Expanded Concepts")
            st.write(res["expanded_concepts"])

            st.subheader("Skill / Theory Questions")
            st.write(res["skill_questions"])

            st.subheader("Project-Based Questions")

            if res["project_questions"]:
                for p in res["project_questions"]:

                    st.markdown(f"### {p['project']}")

                    qs = p["questions"]

                    st.write(qs)
                    st.divider()

            else:
                st.info("No project questions generated from resume.")


        else:
            st.error("API Error")
