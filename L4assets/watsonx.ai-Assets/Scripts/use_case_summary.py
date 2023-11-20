"""
author: Elena Lowery

This code sample shows how to invoke Large Language Models (LLMs) deployed in watsonx.ai.
Documentation: # https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html#
You will need to provide your IBM Cloud API key and a watonx.ai project id (any project)
for accessing watsonx.ai
This example shows a simple summary use case without comprehensive prompt tuning
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

REVIEW_TYPE_DEFAULT = "Default"
REVIEW_TYPE_NEGATIVE = "Negative"
REVIEW_TYPE_POSITIVE = "Positive"
REVIEW_TYPE_KEYWORD_INTEREST = "Interest Rate"
REVIEW_TYPE_BULLET_POINTS = "Bullet Points"

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

    service_review = f"""
    I started my loan process toward securing a VA loan. 
    I was waiting for a a month and a couple weeks, then I was told that the VA needed  
    to acquire my retirement points to verify my veteran status. If I knew this is what 
    my loan was on hold for, I could have contacted the VA office right away and got this cleared up. 
    For whatever reason, it took the underwriting department a long time to verify my employment status, 
    even after I uploaded a couple years of my W2 forms from both of my jobs, and they had my 
    Social Security number to further verify my employment status. My loan completion date 
    was extended, because I wasn't made aware that they were waiting for my VA status to be approved. 
    The push back for my mortgage is common for mortgage companies, but this caused my interest rate to go up. 
    Then, the securing of a closing lawyer being made aware to me and the lawyer needing three days to 
    get their end prepared for me to go to their office to sign the paperwork wasn't made aware to me. 
    My loan missed the second closing date. For whatever reason, the locked in interest rate jumped up 5/8 points. 
    After making the banker I was working with aware of this, he didn't understand why the locked in 
    interest rate jumped up either. He was nice enough to work on it and was able to get the interest 
    rate down in 1/4 of a point, so my mortgage has an interest rate that is 3/8 of a point higher 
    than my locked in interest rate in the beginning of this process. Although my interest rate is 
    higher than the locked in interest point, at the end, the mortgage is successfully finished.
    """

    return service_review

# This function constructs a zero-shot prompt for the LLM
def get_prompt(service_review, review_type):

    # Get the complete prompt by replacing variables

    if review_type == REVIEW_TYPE_BULLET_POINTS:
        # Few shot prompting - this type of review is the most challenging one for an LLM
        # That's why we provide a few examples
        complete_prompt = get_few_shot_prompt(service_review)
        # Read from file (use either the hardcoded string function (comment out the other one)
        # complete_prompt = get_few_shot_prompt_from_file(review, "\\prompt_templates\\few_shot_summary.txt")
    else:
        complete_prompt = f"""
            Generate a short summary of a service review to give feedback to the customer service department.\n
            Summarize the review below, delimited by ''' , in at most 100 words, and focusing on {review_type} comments.\n
            Review: ```{service_review}```
            """

    return complete_prompt

# This function constructs a few-shot prompt for the LLM
def get_few_shot_prompt(service_review):

    # We hardcoded the prompt for quick testing. See the get_few_shot_prompt_from_file() for a better approach

    complete_prompt = f"""
    Please provide top 5 bullet points in the review provided in '''.

    Review:
    '''I had 2 problems with my experience with my refinance. 1) The appraisal company used only tried to lower my house value to fit the comps that he was able to find in the area. My house is unique and he did not use the unique pictures to compare value. He purposely left them out of the appraisal. 2) I started my loan process on a Thursday. On Saturday I tried to contact my loan officer to tell him of the American Express offer that I wanted to apply for. I was informed that it was too late and I could not use it because it would delay the process. I had just received the email about the offer and I had just started the process so how was it too late to get in on the $2,000 credit on my current bill. I let it go but I should have dropped the process and restarted it because that would have helped me out with my bill'''

    Top bullet points: 
    1. The appraisal company undervalued the reviewer's house by purposely excluding unique pictures that would have accurately assessed its value.
    2. The uniqueness of the house was not taken into consideration, and the appraiser relied solely on comps that did not reflect its true worth.
    3. The reviewer attempted to inform their loan officer about an American Express offer they wanted to apply for, which would have provided a $2,000 credit on their current bill.
    4. The loan officer stated it was too late to take advantage of the offer as it would delay the process, despite the reviewer having just received the email and recently started the loan process.
    5. The reviewer regrets not dropping the process and restarting it to benefit from the offer, as it would have helped them with their bill.

    Review:'''
    For the most part my experience was very quick and very easy. I did however, have 3 issues.

    #1 - When I received my final numbers, my costs were over $2000 more than was quoted to me over the phone. This was straightened out quickly and matched what I was quoted.

    #2 - The appraiser had to change his schedule and when I didn't know if I could be home for the appraisal, he said he could do it with me not there. I do not think this is a wise thing to do or to offer.
    
    #3 - When I received my appraisal, it was far lower than it should have been. My house appraised for basically the same price I purchased it for 14 years ago. I have kept the home up with flooring, paint, etc. It has new shingles on it from last summer, the driveway has been paved, I have about three acres landscaped compared to maybe one when I bought it, and have paved the driveway which was originally gravel.
    
    Even if you discount the insanely high prices that houses are selling for in today's market, the house has increased in value over the past fourteen years. In fact, some of the compared properties looked like camps that were not on water, had no basement or possibly no slab, and very minimal acreage. These comparably priced houses were in no way equal to my 4 bedroom cape, with a wraparound deck, on 4 acres, though not on the water, it is overlooking lake around 100 feet away at the most. I feel very strongly that the appraisal price was put in at a high enough estimate to satisfy the needs of the refinance loan.'''
    
    Top bullet points:
    1. Overall, the experience was quick and easy, but there were three specific issues.
    2. Initially, the quoted costs over the phone did not match the final numbers, resulting in a discrepancy of over $2000. However, this was promptly resolved.
    3. The appraiser offered to conduct the appraisal without the homeowner present, which the reviewer felt was unwise and not recommended.
    4. The appraisal value of the house was significantly lower than expected, even considering the current high housing market prices. The reviewer mentioned various upgrades and improvements made to the house over the past 14 years.
    5. The reviewer expressed a strong belief that the appraisal was deliberately set at a lower value to meet the requirements of the refinance loan, despite the property's unique features and advantages compared to the comparables used.
    
    
    Review:'''
    I was told upfront and throughout most of the process that I would be able to get a $25K payout/cash back based on the market value of my house that was discussed in the original conversation with the loan officer. However, midway into the process I was told by the loan officer that I was only able to get $17.5K back. Additionally, I was told that I would be able to skip 2 months of mortgage payment to help makeup for the cash shortage. However, at the end of the day I was told that I could only skip 1 mortgage payment. These 2 drawbacks caused me to not fully satisfy the financial reason of why I originally wanted to refinance which was to get the $25K cash.
    
    Top bullet points:
    1. The initial agreement with the loan officer stated that the reviewer would receive a $25K cash payout based on the market value of their house.
    2. Midway through the process, the loan officer informed the reviewer that they would only be eligible for a $17.5K cash payout, which was lower than initially discussed.
    3. The reviewer was also promised the ability to skip two months of mortgage payments to compensate for the cash shortage, but they were later informed that they could only skip one payment.
    4. These discrepancies in the cash payout amount and the reduced mortgage payment relief prevented the reviewer from fulfilling their original financial objective of obtaining the $25K cash.
    5. The limitations and changes in the terms impacted the overall satisfaction with the refinancing process and compromised the financial benefits the reviewer had anticipated.
    
    Review: ```{service_review}```
    
    Top bullet points:
    """

    return complete_prompt

# This function is not called by default, however, you can use it if you put your prompt text in a file
def get_few_shot_prompt_from_file(review, fileName):

    # Retrieving prompts from a file is a better option than hardcoding them,

    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # For troubleshooting
    # print("Script dir: " + script_dir)

    # Construct the absolute path of the text file
    file_path = script_dir + fileName
    # for troubleshooting
    # print("Absolute path: " + file_path)

    # Read the contents of the text file
    with open(file_path, 'r') as file:
        prompt = file.read()
    # for troubleshooting
    # print("Retrieved prompt from template: " + prompt)

    complete_prompt = prompt + "Review: ```" + review + "```Top bullet points:"
    # for troubleshooting
    # print("Prompt retrieved from file: " + complete_prompt)

    return complete_prompt

def main():

    # Get the review that we will summarize
    review = get_review()

    # Create prompts for different types of summary
    complete_prompt1 = get_prompt(review, REVIEW_TYPE_DEFAULT)
    complete_prompt2 = get_prompt(review, REVIEW_TYPE_NEGATIVE)
    complete_prompt3 = get_prompt(review, REVIEW_TYPE_POSITIVE)
    complete_prompt4 = get_prompt(review, REVIEW_TYPE_KEYWORD_INTEREST)
    complete_prompt5 = get_prompt(review, REVIEW_TYPE_BULLET_POINTS)

    # Specify model parameters
    model_type = ModelTypes.FLAN_UL2
    max_tokens = 300
    min_tokens = 50
    decoding = DecodingMethods.SAMPLE
    temperature = 0.7

    # Get the API key and project id and update global variables
    get_credentials()

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    # Default summary
    # Invoke the model and print the results
    generated_response = model.generate(prompt=complete_prompt1)
    # print model response
    print("--------------------------------- Default Review Summary -----------------------------------")
    print("Prompt: " + complete_prompt1.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Default Summary: " + generated_response['results'][0]['generated_text'])
    print("*********************************************************************************************")

    # Negative summary
    # Invoke the model and print the results
    generated_response = model.generate(prompt=complete_prompt2)
    # print model response
    print("--------------------------------- Negative Review Summary -----------------------------------")
    print("Prompt: " + complete_prompt1.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Negative Summary: " + generated_response['results'][0]['generated_text'])

    # Positive summary
    # Invoke the model and print the results
    generated_response = model.generate(prompt=complete_prompt3)
    # print model response
    print("--------------------------------- Positive Review Summary -----------------------------------")
    print("Prompt: " + complete_prompt1.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Positive Summary: " + generated_response['results'][0]['generated_text'])

    # Keyword summary
    # Invoke the model and print the results
    generated_response = model.generate(prompt=complete_prompt4)
    # print model response
    print("--------------------------------- Keyword  Summary -----------------------------------")
    print("Prompt: " + complete_prompt1.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Keyword Summary: " + generated_response['results'][0]['generated_text'])

    # Bullet points summary
    # Invoke the model and print the results
    generated_response = model.generate(prompt=complete_prompt5)
    # print model response
    print("--------------------------------- Bullet Points Summary -----------------------------------")
    print("Prompt: " + complete_prompt1.strip())
    print("---------------------------------------------------------------------------------------------")
    print("Bullet Points Summary: " + generated_response['results'][0]['generated_text'])

    # Test modular function invocation
    get_summary(api_key, watsonx_project_id, review,REVIEW_TYPE_DEFAULT,model_type)

# This function is called when this script is imported as a module
def get_summary(request_api_key, request_project_id, review,review_type,model_type):

    # Update the global variable
    globals()["api_key"] = request_api_key
    globals()["watsonx_project_id"] = request_project_id

    # Specify model parameters
    max_tokens = 300
    min_tokens = 50
    decoding = DecodingMethods.SAMPLE
    temperature = 0.7

    # Instantiate the model
    model = get_model(model_type, max_tokens, min_tokens, decoding, temperature)

    complete_prompt = get_prompt(review, review_type)

    generated_response = model.generate(prompt=complete_prompt)
    response_text = generated_response['results'][0]['generated_text']

    print("Prompt: " + complete_prompt)
    print("*************************************************************")
    print("Function invocation test result:" + response_text)

    return response_text

# Invoke the main function
if __name__ == "__main__":
    main()
