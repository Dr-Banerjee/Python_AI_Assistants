import streamlit as st
import pdfplumber
from openai import OpenAI
from config import git  #put your own github token in the config file to use chat-gpt


def text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def get_response(input_prompt):
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=git,
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an ATS (Application Tracking System) expert."},
            {"role": "user", "content": input_prompt},
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    return response.choices[0].message.content


st.title("ATS Resume Analyzer")
st.text("Improve your resume based on job description")

jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf", help="Please upload a PDF file.")

submit = st.button("Submit")

if submit:
    if not jd:
        st.warning("Please enter a job description.")
    elif not uploaded_file:
        st.warning("Please upload your resume.")
    else:
        resume_text = text_from_pdf(uploaded_file)

        if not resume_text:
            st.error("Can't extract text")
        else:
            input_prompt = (
                f"Assume you are an advanced ATS specializing in tech roles (software engineering, data science, and data analysis). "
                f"Evaluate the following resume based on the given job description. "
                f"Assign a percentage match and list missing keywords for improvement.\n\n"
                f"Resume:\n{resume_text}\n\n"
                f"Job Description:\n{jd}"
            )

            response = get_response(input_prompt)
            st.subheader("Feedback:")
            st.write(response)
