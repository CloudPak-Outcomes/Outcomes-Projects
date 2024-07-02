"""
author: Elena Lowery

This code sample shows how to invoke Large Language Models (LLMs) deployed in watsonx.ai.
Documentation: https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html
You will need to provide your IBM Cloud API key and a watonx.ai project id  (any project)
for accessing watsonx.ai in a .env file
This example shows simple use cases without comprehensive prompt tuning
"""

# Install the wml api your Python env prior to running this example:
# pip install ibm-watson-machine-learning
# pip install ibm-cloud-sdk-core

# In non-Anaconda Python environments, you may also need to install dotenv
# pip install python-dotenv

# For reading credentials from the .env file.\
import os
from dotenv import load_dotenv
# WML python SDK
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

# For invocation of LLM with REST API
import requests, json
from ibm_cloud_sdk_core import IAMTokenManager

# Important: hardcoding the API key in Python code is not a best practice. We are using
# this approach for the ease of demo setup. In a production application these variables
# can be stored in an .env or a properties file

# URL of the hosted LLMs is hardcoded because at this time all LLMs share the same endpoint
url = "https://us-south.ml.cloud.ibm.com"

# These global variables will be updated in get_credentials() functions
watsonx_project_id = ""
# Replace with your IBM Cloud key
api_key = ""

def get_credentials():

    load_dotenv()

    # Update the global variables that will be used for authentication in another function
    globals()["api_key"] = os.getenv("api_key", None)
    globals()["watsonx_project_id"] = os.getenv("project_id", None)

# The get_model function creates an LLM model object with the specified parameters
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

def get_list_of_complaints():

    # Look up parameters in documentation:
    # https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html#

    # You can specify any prompt and change parameters for different runs

    # If you want the end user to have a choice of the number of tokens in the output as well as decoding
    # and temperature, you can parameterize these values

    model_type = ModelTypes.FLAN_UL2
    max_tokens = 100
    min_tokens = 50
    decoding = DecodingMethods.GREEDY
    # Temperature will be ignored if GREEDY is used
    temperature = 0.7

    # Instantiate the model
    model = get_model(model_type,max_tokens,min_tokens,decoding, temperature)

    complaint = f"""
            I just tried to book a flight on your incredibly slow website.  All 
            the times and prices were confusing.  I liked being able to compare 
            the amenities in economy with business class side by side.  But I 
            never got to reserve a seat because I didn't understand the seat map.  
            Next time, I'll use a travel agent!
            """

    # Hardcoding prompts in a script is not best practice. We are providing this code sample for simplicity of
    # understanding

    prompt_get_complaints = f"""
    From the following customer complaint, extract 3 factors that caused the customer to be unhappy. 
    Put each factor on a new line. 

    Customer complaint:{complaint}

    Numbered list of all the factors that caused the customer to be unhappy:

    """

    # Invoke the model and print the results
    generated_response = model.generate(prompt=prompt_get_complaints)
    # WML API returns a dictionary object. Generated response is a list object that contains generated text
    # as well as several other items such as token count and seed
    # We recommmend that you put a breakpoint on this line and example the result object
    print("---------------------------------------------------------------------------")
    print("Prompt: " + prompt_get_complaints)
    print("List of complaints: " + generated_response['results'][0]['generated_text'])
    print("---------------------------------------------------------------------------")

def answer_questions():

    # Look up parameters in documentation:
    # https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html#

    # You can specify any prompt and change parameters for different runs

    # If you want the end user to have a choice of the number of tokens in the output as well as decoding
    # and temperature, you can parameterize these values

    final_prompt = "Write a paragraph about the capital of France."
    model_type = ModelTypes.FLAN_UL2
    max_tokens = 300
    min_tokens = 50
    decoding = DecodingMethods.SAMPLE
    temperature = 0.7

    # Instantiate the model
    model = get_model(model_type,max_tokens,min_tokens,decoding, temperature)
    # Invoke the model and print the results
    generated_response = model.generate(prompt=final_prompt)
    # WML API returns a dictionary object. Generated response is a list object that contains generated text
    # as well as several other items such as token count and seed
    # We recommmend that you put a breakpoint on this line and example the result object
    print("---------------------------------------------------------------------------")
    print("Question/request: " + final_prompt)
    print("Answer: " + generated_response['results'][0]['generated_text'])
    print("---------------------------------------------------------------------------")

def invoke_with_REST():

    rest_url ="https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-29"

    access_token = get_auth_token()

    model_type = "google/flan-ul2"
    
    max_tokens = 300
    min_tokens = 50
    decoding = "sample"
    temperature = 0.7

    final_prompt = "Write a paragraph about the capital of France."

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
        }

    data = {
        "model_id": model_type,
        "input": final_prompt,
        "parameters": {
            "decoding_method": decoding,
            "max_new_tokens": max_tokens,
            "min_new_tokens": min_tokens,
            "temperature": temperature,
            "stop_sequences": ["."],
            },
        "project_id": watsonx_project_id
    }

    response = requests.post(rest_url, headers=headers, data=json.dumps(data))
    generated_response = response.json()['results'][0]['generated_text']

    print("--------------------------Invocation with REST-------------------------------------------")
    print("Question/request: " + final_prompt)
    print("Answer: " + generated_response)
    print("---------------------------------------------------------------------------")

def get_auth_token():

    # Access token is required for REST invocation of the LLM
    access_token = IAMTokenManager(apikey=api_key,url="https://iam.cloud.ibm.com/identity/token").get_token()
    return access_token

def demo_LLM_invocation():

    # Load the api key and project id
    get_credentials()

    # Show examples of 2 use cases/prompts
    answer_questions()
    get_list_of_complaints()

    # Simple prompt - invoked with the REST API
    invoke_with_REST()

demo_LLM_invocation()