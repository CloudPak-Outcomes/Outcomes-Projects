"""
author: Elena Lowery

This code sample shows how to invoke Large Language Models (LLMs) deployed in watsonx.ai.
Documentation: # https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html#
You will need to provide your IBM Cloud API key and a watonx.ai project id (any project)
for accessing watsonx.ai
This example shows a Generate use case
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

TASK_DEFAULT = "default"
TASK_GENERATE_EMAIL = "generate email"

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

def get_review():

    # This code can be replaced with getting a review from a file or another sources
    # Source of this review: DeepLearningAI Prompt Class example https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/7/expanding

    # Try different types of reviews - one at a time or modify the code to read from file.

    # review for a blender
    service_review = f"""
    So, they still had the 17 piece system on seasonal sale for around $49 in the month of
    November, about  half off, but for some reason (call it price gouging) 
    around the second week of December the prices all went up to about anywhere from 
    between $70-$89 for the same system. And the 11 piece system went up around $10 or 
    so in price also from the earlier sale price of $29. So it looks okay, but if you look at the base, the part 
    where the blade locks into place doesn’t look as good as in previous editions from a few years ago, but I 
    plan to be very gentle with it (example, I crush very hard items like beans, ice, rice, etc. in the 
    blender first then pulverize them in the serving size I want in the blender then switch to the whipping 
    blade for a finer flour, and use the cross cutting blade first when making smoothies, then use the flat blade 
    if I need them finer/less pulpy). Special tip when making smoothies, finely cut and freeze the fruits and 
    vegetables (if using spinach-lightly stew soften the spinach then freeze until ready for use-and if making 
    sorbet, use a small to medium sized food processor) that you plan to use that way you can avoid adding so 
    much ice if at all-when making your smoothie. After about a year, the motor was making a funny noise. 
    I called customer service but the warranty expired already, so I had to buy another one. FYI: The overall 
    quality has gone done in these types of products, so they are kind of counting on brand recognition and 
    consumer loyalty to maintain sales. Got it in about two days.
    """

    return service_review

def get_prompt(service_review, task_type, sentiment):

    # Get the complete prompt by replacing variables

    if task_type == TASK_GENERATE_EMAIL:
        complete_prompt = f"""
        You are a customer service AI assistant. Your task is to generate an email reply to the customer.
        Using text delimited by ``` Generate a reply to thank the customer for their review.
        
        If the sentiment is positive or neutral, thank them for their review.
        If the sentiment is negative, apologize and suggest that they can reach out to customer service. 
        
        Use specific details from the review.
        
        Write in a concise and professional tone.
        
        Sign the email as `AI customer agent`.
        Customer review: ```{service_review}```
        Review sentiment: {sentiment}
        """
    else:
        # Provide a summary of the text
        complete_prompt = f"""
        Summarize the review below, delimited by ''' , in at most 100 words.
        Review: ```{service_review}```
        """

    return complete_prompt

def main():

    # Specify model parameters
    model_type = ModelTypes.MPT_7B_INSTRUCT2
    max_tokens = 150
    min_tokens = 100
    decoding = DecodingMethods.SAMPLE
    temperature = 0.7

    # Get the API key and project id and update global variables
    get_credentials()

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    review = get_review()
    complete_prompt = get_prompt(review, TASK_GENERATE_EMAIL, "negative")

    generated_response = model.generate(prompt=complete_prompt)
    response_text = generated_response['results'][0]['generated_text']

    # print model response
    print("--------------------------------- Generated email for a negative review -----------------------------------")
    print("Prompt: " + complete_prompt.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Generated email: " + response_text)
    print("*********************************************************************************************")

    # Test invocation of a function from the external moduel
    generate(api_key,watsonx_project_id,review,TASK_GENERATE_EMAIL,model_type)

def generate(request_api_key, request_project_id, review, task,model_type):

    # Update the global variable
    globals()["api_key"] = request_api_key
    globals()["watsonx_project_id"] = request_project_id

    # Specify model parameters
    max_tokens = 150
    min_tokens = 100
    decoding = DecodingMethods.SAMPLE
    temperature = 0.7

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    complete_prompt = get_prompt(review, task, "negative")

    generated_response = model.generate(prompt=complete_prompt)
    response_text = generated_response['results'][0]['generated_text']

    print("*************************************************************")
    print("Function invocation test result:" + response_text)


# Invoke the main function
if __name__ == "__main__":
    main()
