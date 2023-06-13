import requests
from cpdalllibs.cpdaaslib.constants import *

def getToken(key) :
    """Get the access token required to interface with CPDaaS"""
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/x-www-form-urlencoded'
    }
    data = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={}"
    resp = requests.post(IAM_ENDPOINT + '/identity/token', 
                        headers=headers, data=data.format(key))

    return(resp)

def apikeyDetails(API_key, access_token) :
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'IAM-Apikey' : API_key
    }
    resp = requests.get(IAM_ENDPOINT + '/v1/apikeys/details', headers=headers)
    return(resp)

def accountConfig(headersAPI, account_id) :
    endpoint = IAM_ENDPOINT + '/v1/accounts/{}/settings/identity?include_history=false'
    resp = requests.get(endpoint.format(account_id), headers=headersAPI)
    return(resp)

def getServiceIDs(headersAPI, account_id) :
    endpoint = IAM_ENDPOINT + '/v1/serviceids?pagesize=100&account_id={}'
    resp = requests.get(endpoint.format(account_id), headers=headersAPI)
    if resp.status_code > 204 :
        print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
        return []
    resp_json = resp.json()
    total = resp_json['serviceids']
    while 'next' in resp_json :
        resp = requests.get(resp_json['next'], headers=headersAPI)
        resp_json = resp.json()
        total.extend(resp_json['serviceids'])
    return(total)