"""
author: Elena Lowery

This code sample shows how to invoke Large Language Models (LLMs) deployed in watsonx.ai.
Documentation: # https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html#
You will need to provide your IBM Cloud API key and a watonx.ai project id (any project)
for accessing watsonx.ai
This example shows a Question and Answer use case for a provided document

"""

# For reading credentials from the .env file
import os
from dotenv import load_dotenv

import streamlit as st
import use_case_RAG_Web

# URL of the hosted LLMs is hardcoded because at this time all LLMs share the same endpoint
url = "https://us-south.ml.cloud.ibm.com"

# These global variables will be updated in get_credentials() function
watsonx_project_id = ""
# Replace with your IBM Cloud key
api_key = ""

def get_credentials():

    load_dotenv()
    # Update the global variables that will be used for authentication in another function
    globals()["api_key"] = os.getenv("api_key", None)
    globals()["watsonx_project_id"] = os.getenv("project_id", None)


def main():

    # Get the API key and project id and update global variables
    get_credentials()

    # Use the full page instead of a narrow central column
    st.set_page_config(layout="wide")

    # Streamlit app title
    st.title("🌠Demo of RAG with a Web page")

    user_url = st.text_input('Provide a URL')

    collection_name = st.text_input('Provide a unique name for this website (lower case). Use the same name for the same URL to avoid loading data multiple times.')

    # UI component to enter the question
    question = st.text_area('Question',height=100)
    button_clicked = st.button("Answer the question")

    st.subheader("Response")

    # Invoke the LLM when the button is clicked
    if button_clicked:
        response = use_case_RAG_Web.answer_questions_from_web(api_key,watsonx_project_id,user_url,question,collection_name)
        st.write(response)

if __name__ == "__main__":
    main()


