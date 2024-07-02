"""
author: Elena Lowery

This code sample shows how to invoke Large Language Models (LLMs) deployed in watsonx.ai.
Documentation: # https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html#
You will need to provide your IBM Cloud API key and a watonx.ai project id (any project)
for accessing watsonx.ai
This example shows several examples of inference with LLMs
"""

# Install the wml api your Python env prior to running this example:
# pip install ibm-watson-machine-learning

# For reading credentials from the .env file
import os
from dotenv import load_dotenv

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

# Important: hardcoding the API key in Python code is not a best practice. We are using
# this approach for the ease of demo setup. In a production application these variables
# can be stored in an .env or a properties file

# URL of the hosted LLMs is hardcoded because at this time all LLMs share the same endpoint
url = "https://us-south.ml.cloud.ibm.com"

TASK_SENTIMENT = "Sentiment"
TASK_EMOTIONS = "Emotions"
TASK_ENTITY = "Entities"

# These global variables will be updated in get_credentials() function
watsonx_project_id = ""
# Replace with your IBM Cloud key
api_key = ""

def get_credentials():

    load_dotenv()

    # Update the global variables that will be used for authentication in another function
    globals()["api_key"] = os.getenv("api_key", None)
    globals()["watsonx_project_id"] = os.getenv("project_id", None)

# This function creates a model object with the specified parameters
def get_model(model_type,max_tokens,min_tokens,decoding,temperature,repetition_penalty):

    generate_params = {
        GenParams.MAX_NEW_TOKENS: max_tokens,
        GenParams.MIN_NEW_TOKENS: min_tokens,
        GenParams.DECODING_METHOD: decoding,
        GenParams.TEMPERATURE: temperature,
        GenParams.REPETITION_PENALTY:repetition_penalty
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


def get_review():

    # This code can be replaced with getting a review from a file or another sources
    # Source of this review: https://www.consumeraffairs.com

    # Try different types of reviews - one at a time or modify the code to read from file.

    # service_review = f"""
    # This is a great full service hotel. But, amazingly they do not have an oceanfront handicap accessible room.
    # I rented 4 rooms for a family get together, but for us, the parents/grandparents who sponsored and paid
    # for this otherwise fun occasion, we had to struggle with too low toilets, (they brought a riser),
    # not being able to use shower or even sink, impossible doors, and no access to deck,
    # just so we could have an oceanfront room. Yes we knowingly made that trade,
    # but a hotel of this caliber in this America in this day and age could surely
    # offer a handicap accessible room in each major room category.
    # I am disappointed in Hilton, even as a gold honors member.
    # They could do better for those of us less fortunate.
    # """

    service_review = f"""
    We used the Hilton Waikoloa's pool and slide while vacationing at the HGV Kingsland. 
    The property was really overwhelming and quite huge. They had a train and boat to get 
    around since it was so big. Our girls loved the slide at the pool and also swimming with the dolphins. 
    The lagoon kiosk rented some snorkels which was very easy since there were no waves inside the lagoon. 
    Lots of turtles there! Food was the only downside as it is very expensive. 
    But I guess it was expected since it is Hawaii. We would love to return once they have 
    the Oceans Tower timeshares built for the HGV Club. Especially with the ocean views!
    """

    return service_review

# This function creates a complete prompt
def get_prompt(service_review, task_type):

    # Get the complete prompt by replacing variables

    if task_type == TASK_SENTIMENT:
        complete_prompt = f"""
            What is the sentiment of the following product review, which is delimited by '''.
            Answer with a single word, either "positive" or "negative".
            Review: ```{service_review}```
            """
    elif task_type == TASK_EMOTIONS:
        complete_prompt = f"""
            Identify a list of emotions in text delimited by '''. 
            Include no more than 5 items in the list. 
            Format your answer as a list of lower-case words separated by commas.
            Review: ```{service_review}```
            """
    elif task_type == TASK_ENTITY:
        complete_prompt = f"""
            Identify the following items from the review text: city, hotel name
            Review: ```{service_review}```
            """
    else:
        # Provide a summary of the review
        complete_prompt = f"""
            Generate a short summary of a service review to give feedback to the customer service department.
            Summarize the review below, delimited by ''' , in at most 100 words.
            Review: ```{service_review}```
            """

    return complete_prompt

def main():

    # Specify model parameters
    model_type = ModelTypes.FLAN_UL2
    max_tokens = 70
    min_tokens = 30
    decoding = DecodingMethods.GREEDY
    temperature = 0.7
    # Max repition penalty, 1 is min
    repetition_penalty = 2

    # Get the API key and project id and update global variables
    get_credentials()

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature,repetition_penalty)

    # Get sample review
    review = get_review()

    # Construct prompts
    complete_prompt1 = get_prompt(review, TASK_SENTIMENT)
    complete_prompt2 = get_prompt(review, TASK_EMOTIONS)
    complete_prompt3 = get_prompt(review, TASK_ENTITY)

    # Invoke the model
    generated_response = model.generate(prompt=complete_prompt1)
    response_text = generated_response['results'][0]['generated_text']
    # print model response
    print("--------------------------------- Sentiment -----------------------------------")
    print("Prompt: " + complete_prompt1.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Review sentiment: " + response_text)
    print("*********************************************************************************************")

    # Emotions
    generated_response = model.generate(prompt=complete_prompt2)
    response_text = generated_response['results'][0]['generated_text']
    # print model response
    print("--------------------------------- Emotions -----------------------------------")
    print("Prompt: " + complete_prompt2.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Emotions: " + response_text)
    print("*********************************************************************************************")

    # Entity
    generated_response = model.generate(prompt=complete_prompt3)
    response_text = generated_response['results'][0]['generated_text']
    # print model response
    print("--------------------------------- Entities -----------------------------------")
    print("Prompt: " + complete_prompt3.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Entities Summary: " + response_text)
    print("*********************************************************************************************")

    # Test the function that will be invoked from the module
    # Test modular function invocation
    extract(api_key, watsonx_project_id, review, TASK_ENTITY,model_type)

# Function that can be invoked from external modules
def extract(request_api_key, request_project_id, review, task_type,model_type):

    # Update the global variable
    globals()["api_key"] = request_api_key
    globals()["watsonx_project_id"] = request_project_id

    # Specify model parameters
    max_tokens = 100
    min_tokens = 30
    decoding = DecodingMethods.GREEDY
    temperature = 0.7
    # Max repition penalty, 1 is min
    repetition_penalty = 2

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature, repetition_penalty)

    # Construct the prompt
    complete_prompt = get_prompt(review, task_type)

    # Invoke the model
    generated_response = model.generate(prompt=complete_prompt)
    response_text = generated_response['results'][0]['generated_text']

    return response_text

# Invoke the main function
if __name__ == "__main__":
    main()
