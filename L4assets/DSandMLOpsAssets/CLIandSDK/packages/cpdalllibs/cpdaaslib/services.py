import requests
from requests.structures import CaseInsensitiveDict
from cpdalllibs.cpdaaslib.constants import *
import json

def listGlobalCatalog(headersAPI, limit) :
    '''List some entries from the global catalog'''
    endpoint = GLOBAL_CATALOG_ENDPOINT + \
        '?limit={}&languages=en-us&q=tag:watson+kind:service'.format(limit)
    resp = requests.get(endpoint, headers=headersAPI)
    return resp

def getServiceInstances(headersAPI) :
    '''Get all the services part of this account'''
    resp = requests.get(RESOURCE_ENDPOINT + '/v2/resource_instances', headers=headersAPI)
    if resp.status_code > 202 :
        print("Status code: {}, reason: {}\n".format(resp.status_code,resp.reason))
    return resp.json()

def getAccessGroups(headersAPI, account_id) :
    limit = 100 # max value: 100
    access_group_json = []
    resp = requests.get(IAM_ENDPOINT + 
                    '/v2/groups?account_id={}&limit={}'.format(account_id,limit), 
                    headers=headersAPI)
    if resp.status_code > 202 : # if error
        print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
    else :
        resp_json = resp.json()
        access_group_json = resp_json['groups']
        while 'next' in resp_json :
            resp = requests.get(resp_json['next']['href'], headers=headersAPI)
            resp_json = resp.json()
            access_group_json.extend(resp_json['groups'])
    return access_group_json

def getServiceIds(headersAPI, account_id) :
    pagesize=100 # max value, default 20
    service_ids = []
    resp = requests.get(IAM_ENDPOINT + '/v1/serviceids?account_id={}&pagesize={}'.format(account_id,pagesize), 
                        headers=headersAPI)
    resp_json = resp.json()
    if resp.status_code > 202 : # if error
        print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
        print(json.dumps(resp_json, indent=2, sort_keys=True))
    else :
        resp_json = resp.json()
        service_ids = resp_json['serviceids']
        while 'next' in resp_json :
            resp = requests.get(resp_json['next'], headers=headersAPI)
            resp_json = resp.json()
            service_ids.extend(resp_json['serviceids'])
    return(service_ids)

def addDVUser(email,DV_header):
    '''Add user to data virtualization'''
    payload = {"dvRole": "DV_WORKER", "iam": True, "ibmid": "user@us.ibm.com" }
    payload['ibmid'] = email
    resp = requests.post(DV_ENDPOINT + '/dbapi/v4/users', json=payload, headers=DV_header)
    print("{}: Status code: {}, reason: {}".format(email,resp.status_code,resp.reason))
    if resp.status_code > 204 :
        print(resp.text)
    return(resp)

def addOpenscaleUser(iam_id, account_id, os_guid, headersAPI) :
    ''' Add a user to openscale'''
    data = {
        "type": "access",
        "subjects": [{
            "attributes": [{
                "name": "iam_id",
                "value": iam_id
            }]
        }],
        "roles": [{"role_id": "crn:v1:bluemix:public:iam::::role:Viewer"}],
        "resources": [{
            "attributes": [{
                "name": "accountId",
                "value": account_id,
                "operator": "stringEquals"
            },
                {
                "name": "serviceName",
                    "value": "aiopenscale"
            },
                {
                "name": "serviceInstance",
                    "value": os_guid,
                    "operator": "stringEquals"
            }]
        }]
    }
    resp = requests.post(IAM_ENDPOINT + '/v1/policies', json=data, headers=headersAPI)
    #print("{}: Status code: {}, reason: {}".format(iam_id,resp.status_code,resp.reason))
    return(resp)