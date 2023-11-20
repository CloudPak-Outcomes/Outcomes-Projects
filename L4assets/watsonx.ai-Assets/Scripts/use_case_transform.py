"""
author: Elena Lowery

This code sample shows how to invoke Large Language Models (LLMs) deployed in watsonx.ai.
Documentation: # https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html#
You will need to provide your IBM Cloud API key and a watonx.ai project id (any project)
for accessing watsonx.ai
This example shows a Transform use case
"""

# Install the wml api your Python env prior to running this example:
# pip install ibm-watson-machine-learning

# For reading credentials from the .env file
import os
from dotenv import load_dotenv

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

# URL of the hosted LLMs is hardcoded because at this time all LLMs share the same endpoint
url = "https://us-south.ml.cloud.ibm.com"

TASK_BULLET_POINTS = "points"
TASK_COMPLEX_JSON_FORMAT = "json"
TASK_HTML_FORMAT = "html"
TASK_EXTRACT_EMAIL = "email"

# These global variables will be updated in get_credentials() function
watsonx_project_id = ""
# Replace with your IBM Cloud key
api_key = ""

def get_credentials():

    load_dotenv()

    # Update the global variables that will be used for authentication in another function
    globals()["api_key"] = os.getenv("api_key", None)
    globals()["watsonx_project_id"] = os.getenv("project_id", None)

def get_model(model_type,max_tokens,min_tokens,decoding,temperature):

    generate_params = {
        GenParams.MAX_NEW_TOKENS: max_tokens,
        GenParams.MIN_NEW_TOKENS: min_tokens,
        GenParams.DECODING_METHOD: decoding,
        GenParams.TEMPERATURE: temperature
    }

    model = Model(
        model_id=model_type,
        params=generate_params,
        credentials={
            "apikey": api_key,
            "url": url
        },
        project_id=watsonx_project_id
        )

    return model

def get_sample_text(task_type):

    if task_type == TASK_BULLET_POINTS:
        sample_text = f"""
        During the August meetings, we will focus on collecting feedback and requirements for activation. 
        Meeting recordings will be posted in the slack channel. If you would like to join the August meetings, 
        please contact Jane Smith. We are looking forward to collaboration.’‘’
        """
    elif task_type == TASK_HTML_FORMAT:
        sample_text = f"""
        data_json = {{ "resturant employees" :[ 
        {{"name":"Shyam", "email":"shyamjaiswal@gmail.com"}},
        {{"name":"Bob", "email":"bob32@gmail.com"}},
        {{"name":"Jai", "email":"jai87@gmail.com"}}\]}}
        """
    elif task_type == TASK_EXTRACT_EMAIL:
        sample_text = f"""
        WW Team: Elena Lowery, elowery@us.ibm.com
        WW Team: Catherine Cao, catherine.cao@ibm.com
        Another Team: Tech Seller, techseller@ibm.com
        """
    elif task_type == TASK_COMPLEX_JSON_FORMAT:
        sample_text = f"""
        I want you to act as a website content editor. Given the phrase "in [languageName]" I want you to 
        provide the phrase translated into the languages indicated by a list of locales. `languageName` 
        is a variable in the phrase. `[languageName]` should be replaced with the name of the 
        language that relates to the relevant locale. For example, in the en_GB locale `languageName=English`, 
        so the expected translation is "in English". As a second example, in the fr_FR locale, 
        `languageName=francais`, so the expected translation is "en francais". Provide your 
        response as a JSON code block, with the JSON key as the locale, and the JSON value is the translated phrase. 
        Do not write explanations.

        The locales I want you to translate to are:
        en_US, es_US, pt_BR, es_MX, en_MX, en_CA, fr_CA, zh_CN, en_CN, en_AU, en_HK, en_IN, 
        ko_KR, en_MY, en_NZ, en_PH, en_SG, en_TW, zh_TW, th_TH, vi_VN, en_GB, en_EX, de_AT, 
        en_AT, fr_BE, nl_BE, en_BE, bg_BG, cs_CZ, en_CZ, da_DK, en_DK, et_EE, en_FI, fi_FI, en_FR, fr_FR, de_DE.
        
        Output:
        """
    else:
        #
        sample_text = f"""
        Generative AI, or Generative Artificial Intelligence, refers to a subset of artificial intelligence 
        techniques and models that are designed to generate new content, such as text, images, audio, 
        or even video, that resembles human-created content. These models are trained on large datasets 
        and learn the underlying patterns and structures of the data in order to generate new instances 
        that mimic the characteristics of the training data.
        """

    return sample_text

def get_prompt(sample_text, task_type):

    # Get the complete prompt by replacing variables

    if task_type == TASK_BULLET_POINTS:
        complete_prompt = f"""
            Turn each sentence of the following text delimited by ''' into a numbered item:  
            Text: ```{sample_text}```
            """
    elif task_type == TASK_HTML_FORMAT:
        complete_prompt = f"""
            Translate the following python dictionary from JSON to an HTML 
            table with column headers and title: {sample_text}
            """
    elif task_type == TASK_EXTRACT_EMAIL:
        complete_prompt =f"""
            Create a list of email addresses from the following text in '''. Email addresses contain the @ symbol. 
            For example, user1@ibm.com, user2@ibm.com
            Text: {sample_text}
        """
    else:
        # Provide a summary of the text
        complete_prompt = f"""
            Summarize the text below, delimited by ''' , in at most 100 words.
            Text: ```{sample_text}```
            
            Summary: 
            """

    return complete_prompt

def main():

    # Specify model parameters
    model_type = ModelTypes.MPT_7B_INSTRUCT2
    max_tokens = 300
    min_tokens = 30
    decoding = DecodingMethods.GREEDY
    temperature = 0.5

    # Get the API key and project id and update global variables
    get_credentials()

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    sample_text1 = get_sample_text(TASK_BULLET_POINTS)
    sample_text2 = get_sample_text(TASK_HTML_FORMAT)
    sample_text3 = get_sample_text(TASK_EXTRACT_EMAIL)
    sample_text4 = get_sample_text(TASK_COMPLEX_JSON_FORMAT)

    complete_prompt1 = get_prompt(sample_text1, TASK_BULLET_POINTS)
    complete_prompt2 = get_prompt(sample_text2, TASK_HTML_FORMAT)
    complete_prompt3 = get_prompt(sample_text3, TASK_EXTRACT_EMAIL)
    # For the JSON format, the sample text includes the prompt
    complete_prompt4 = sample_text4

    generated_response = model.generate(prompt=complete_prompt1)
    response_text = generated_response['results'][0]['generated_text']

    # print model response
    print("--------------------------------- Bullet points from text -----------------------------------")
    print("Prompt: " + complete_prompt1.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Bullet points from text: " + response_text)
    print("*********************************************************************************************")

    # HTMl format
    generated_response = model.generate(prompt=complete_prompt2)
    response_text = generated_response['results'][0]['generated_text']
    # print model response
    print("--------------------------------- Transformed Format: HTML -----------------------------------")
    print("Prompt: " + complete_prompt2.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Transformed format: " + response_text)
    print("*********************************************************************************************")

    # HTMl format
    generated_response = model.generate(prompt=complete_prompt3)
    response_text = generated_response['results'][0]['generated_text']
    # print model response
    print("--------------------------------- Transformed Format: EMAIL -----------------------------------")
    print("Prompt: " + complete_prompt3.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Transformed format: " + response_text)
    print("*********************************************************************************************")

    # JSON format
    generated_response = model.generate(prompt=complete_prompt4)
    response_text = generated_response['results'][0]['generated_text']
    # print model response
    print("--------------------------------- Transformed Format: JSON -----------------------------------")
    print("Prompt: " + complete_prompt4.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Transformed format: " + response_text)
    print("*********************************************************************************************")

    # Test invocation of a function that will be called from an external module
    transform(api_key,watsonx_project_id,sample_text1,TASK_BULLET_POINTS,model_type)

def transform(request_api_key, request_project_id, sample_text,task,model_type):

    # Update the global variable
    globals()["api_key"] = request_api_key
    globals()["watsonx_project_id"] = request_project_id

    # Specify model parameters
    max_tokens = 300
    min_tokens = 30
    decoding = DecodingMethods.GREEDY
    temperature = 0.5

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    complete_prompt = get_prompt(sample_text,task)

    generated_response = model.generate(prompt=complete_prompt)
    response_text = generated_response['results'][0]['generated_text']

    print("*************************************************************")
    print("Function invocation test result:" + response_text)

    return response_text

# Invoke the main function
if __name__ == "__main__":
    main()

