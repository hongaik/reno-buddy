import streamlit as st
from openai import OpenAI
import os, shutil
from crewai_tools import (
  PDFSearchTool,
  WebsiteSearchTool
)
from crewai import Agent, Task, Crew
from utils import *
st.set_page_config(page_title="Your Trusty Renovation Rules Buddy",page_icon=":hammer:")

if os.path.exists('db'):
    # shutil.rmtree('db')
    for root, dirs, files in os.walk('db'):
        for file in files:
            st.write(os.path.join(root, file))

# <---------- Password Protect ---------->
if not check_password():  
    st.stop()

# <---------- App ---------->

st.title("Welcome 👋!")
st.markdown("I am your friendly HDB Renovation Assistant, Taketa :sunglasses:. Here, you can upload your renovation quotation in PDF and I will review it with HDB's guidelines!")

with st.expander("PLEASE READ DISCLAIMER BEFORE PROCEEDING"):
   st.write(
    """
    IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)

uploaded_file = st.file_uploader("Upload your renovation quotation in PDF", type='pdf')
         
if uploaded_file is not None:
    if is_renovation_quotation(uploaded_file.name).lower() == "no":
        st.warning("Sorry, it doesn't look like you have uploaded a renovation quotation 😔. Please try another document!", icon="⚠️")
    else:
        with st.spinner(f"Evaluating {uploaded_file.name} now! Please give me a minute...😘"):
            assessment_results = review_quotation(uploaded_file.name)
            st.success("Evaluation completed!", icon="✅")
            st.write(assessment_results)

option = st.selectbox(
    "Or try one of these sample documents!",
    (
    "",
    "Basukilam Renovation Quotation.pdf", 
    "Nonsense.pdf"
     )
)

if option == "Basukilam Renovation Quotation.pdf":
    uploaded_file = "sample_renovation_quote.pdf"
elif option == "Nonsense.pdf":
    uploaded_file = "non_sample_renovation_quote.pdf"

if option != "":
    if is_renovation_quotation(uploaded_file).lower() == "no":
        st.warning("Sorry, it doesn't look like you have uploaded a renovation quotation 😔. Please try another document!", icon="⚠️")
    else:
        with st.spinner(f"Evaluating {uploaded_file} now! Please give me a minute...😘"):
            assessment_results = review_quotation(uploaded_file)
            st.success("Evaluation completed!", icon="✅")
            st.write(assessment_results)