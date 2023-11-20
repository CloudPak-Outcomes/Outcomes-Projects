"""
author: Elena Lowery

This code sample shows how to invoke watsonx.ai Generative AI API that's hosted in IBM Cloud.
At this time the API endpoint is hardcoded in the API itself (can't be edited).
You will need to provide your own API key for accessing watsonx.ai
This example shows a simple use cases without comprehensive prompt tuning.
"""

# Install the following libraries in your Python env prior to running this example:
# pip install streamlit

# For reading credentials from the .env file
import os
from dotenv import load_dotenv

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import re

# Modules for invoking LLMs
# We assume that the modules are in the same folder as the streamlit app
import use_case_summary
import use_case_inference

OPTION_SUMMARY = "Summarization"
OPTION_EXTRACT = "Extraction"
OPTION_TRANSFORMATION = "Transformation"
OPTION_GENERATION = "Generation"
OPTION_DOC = "Document Q&A"
OPTION_ANALYZE = "Analyze Data"

REVIEW_TYPE_DEFAULT = "Default"
REVIEW_TYPE_NEGATIVE = "Negative"
REVIEW_TYPE_POSITIVE = "Positive"
REVIEW_TYPE_KEYWORD_INTEREST = "Interest Rate"
REVIEW_TYPE_BULLET_POINTS = "Bullet Points"

TASK_SENTIMENT = "Sentiment"
TASK_EMOTIONS = "Emotions"
TASK_ENTITY = "Entities"

DISPLAY_MODEL_LLAMA = "llama"
DISPLAY_MODEL_GRANITE= "granite"
DISPLAY_MODEL_FLAN = "flan"

# Strings hardcoded in these variables are expected by the WML API
FLAN_UL2 = 'google/flan-ul2'
GRANITE_13B_CHAT = 'ibm/granite-13b-chat-v1'
LLAMA_2_70B_CHAT = 'meta-llama/llama-2-70b-chat'

# These global variables will be updated in get_credentials() function
watsonx_project_id = ""
# Replace with your IBM Cloud key
api_key = ""

# Selected model
selected_use_case_model = ""

def get_credentials():

    load_dotenv()

    # Update the global variables that will be used for authentication in another function
    globals()["api_key"] = os.getenv("api_key", None)
    globals()["watsonx_project_id"] = os.getenv("project_id", None)

def demo_summary():

    # Load images
    # URL of the image file on GitHub
    image_url = "https://github.com/elenalowery/genai/blob/main/img/Review.jpg?raw=true"

    # The layout of hte page is 2 columns
    col1, col2 = st.columns(([1,5]))

    with col1:

        st.header = "Review"
        # Add a dropdown for selecting the review type
        options = [REVIEW_TYPE_DEFAULT, REVIEW_TYPE_NEGATIVE, REVIEW_TYPE_POSITIVE, REVIEW_TYPE_KEYWORD_INTEREST, REVIEW_TYPE_BULLET_POINTS]
        selected_option = st.selectbox("Review type:", options)
        st.image(image_url, use_column_width=True)

        default_review_orig = f"""I started my loan process toward securing a VA loan. I was waiting for a a month
        and a couple weeks, then I was told that the VA needed to acquire my retirement points to verify
        my veteran status. If I knew this is what my loan was on hold for, I could have contacted the VA 
        office right away and got this cleared up. For whatever reason, it took the underwriting department 
        a long time to verify my employment status, even after I uploaded a couple years of my W2 forms 
        from both of my jobs, and they had my Social Security number to further verify my employment status. 
        My loan completion date was extended, because I wasn't made aware that they were waiting for my VA 
        status to be approved. The push back for my mortgage is common for mortgage companies, but this caused my interest rate to go up. 
        Then, the securing of a closing lawyer being made aware to me and the lawyer needing three days to get their end prepared for me to go to their office to sign the paperwork wasn't made aware to me. 
        My loan missed the second closing date. For whatever reason, the locked in interest rate jumped up 5/8 points. 
        After making the banker I was working with aware of this, he didn't understand why the locked in 
        interest rate jumped up either. He was nice enough to work on it and was able to get the interest 
        rate down in 1/4 of a point, so my mortgage has an interest rate that is 3/8 of a point higher 
        than my locked in interest rate in the beginning of this process. Although my interest rate is 
        higher than the locked in interest point, at the end, the mortgage is successfully finished.
        """

        # Clean up the string
        # Remove carriage return characters
        default_review_no_return = re.sub(r'[\n\r]', '', default_review_orig)
        # Remove extra spaces
        default_review = re.sub(r'\s+', ' ', default_review_no_return)

    with col2:
        review = st.text_area('Review',value=default_review, height=300)
        get_summary_clicked = st.button("Summarize")

    st.subheader("Results")

    # Invoke the LLM when the button is clicked
    if get_summary_clicked:
        response = use_case_summary.get_summary(api_key,watsonx_project_id,review,selected_option,selected_use_case_model)
        st.markdown(response, unsafe_allow_html=True)
        #st.write(response)

def demo_extract():

    # Load images
    # URL of the image file on GitHub
    image_url = "https://github.com/elenalowery/genai/blob/main/img/Review.jpg?raw=true"

    # Display images in two columns
    col1, col2 = st.columns(([1,5]))

    with col1:
        st.header = "Extract"
        # Add a select box
        options = [TASK_ENTITY, TASK_EMOTIONS, TASK_SENTIMENT]
        selected_option = st.selectbox("Select an option:", options)
        st.image(image_url, use_column_width=True)

        default_review_orig = f"""We used the Hilton Waikoloa's pool and slide while vacationing at 
        the HGV Kingsland. The property was really overwhelming and quite huge. They had a train 
        and boat to get around since it was so big. Our girls loved the slide at the pool and also 
        swimming with the dolphins. The lagoon kiosk rented some snorkels which was very easy since 
        there were no waves inside the lagoon. Lots of turtles there! Food was the only downside as 
        it is very expensive. But I guess it was expected since it is Hawaii. We would love to return 
        once they have the Oceans Tower timeshares built for the HGV Club. Especially with the ocean views!
        """

        # Clean up the string
        # Remove carriage return characters
        default_review_no_return = re.sub(r'[\n\r]', '', default_review_orig)
        # Remove extra spaces
        default_review = re.sub(r'\s+', ' ', default_review_no_return)

    with col2:
        review = st.text_area('Review',value=default_review, height=300)
        extract_info_clicked = st.button("Extract")

    st.subheader("Results")

    # Invoke the LLM when the button is clicked
    if extract_info_clicked:
        response = use_case_inference.extract(api_key,watsonx_project_id,review,selected_option,selected_use_case_model)
        st.markdown(response, unsafe_allow_html=True)
        #st.write(response)

def get_notes_data():

    # Replace this with the code to invoke the classification scoring job
    file_location = 'https://raw.githubusercontent.com/elenalowery/generative-ai/main/Data/notes_scoring_results.csv'
    categories_df = pd.read_csv(file_location)

    return categories_df
def demo_analyze():

    st.header = "Data Visualization"

    update_analysis = st.button("Run analysis")

    df = pd.DataFrame(get_notes_data())

    # Notify the user that we ran the update:
    if update_analysis:
        # Get the current timestamp
        timestamp = datetime.datetime.now()
        # Format the timestamp as a string
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        st.write("Last update on " + formatted_timestamp)

    # Bar chart
    st.subheader("Types of complaints")
    fig = px.bar(df, x="Category", color="Category", barmode="group")
    st.plotly_chart(fig)

def main():

    # Get the API key and project id and update global variables
    get_credentials()

    # Use the full page instead of a narrow central column
    st.set_page_config(layout="wide")

    # Sidebar
    st.sidebar.title("LLM Use Cases")

    selected_model = st.sidebar.selectbox("Select model",[DISPLAY_MODEL_LLAMA, DISPLAY_MODEL_GRANITE, DISPLAY_MODEL_FLAN])

    if selected_model == DISPLAY_MODEL_LLAMA:
        globals()["selected_use_case_model"] = LLAMA_2_70B_CHAT
    elif selected_model == DISPLAY_MODEL_GRANITE:
        globals()["selected_use_case_model"] = GRANITE_13B_CHAT
    else:
        # Default model if there is no selection
        globals()["selected_use_case_model"] = FLAN_UL2

    # For debugging
    print("Selected model: " + selected_use_case_model)

    selected_option = st.sidebar.selectbox("Select Option", [OPTION_SUMMARY,OPTION_EXTRACT,OPTION_ANALYZE])

    if selected_option == OPTION_SUMMARY:
        demo_summary()
    elif selected_option == OPTION_EXTRACT:
        demo_extract()
    elif selected_option == OPTION_ANALYZE:
        demo_analyze()



if __name__ == "__main__":
    main()
