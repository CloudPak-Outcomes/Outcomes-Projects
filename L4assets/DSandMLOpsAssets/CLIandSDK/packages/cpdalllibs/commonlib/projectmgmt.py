import requests
from cpdalllibs.commonlib.constants import *
import base64
import subprocess

def getProject(headersAPI, guid, url=None, cpdaas=False) :
    """Get a project using a project id"""
    if url is None :
        url = WATSON_DATA_ENDPOINT
    headersAPI['cpdaas-include-permissions'] = "true"
    if url[-1] != "/" :
        url = url + "/"
    endpoint = url + 'v2/projects/{}'.format(guid)
    resp = requests.get(endpoint, headers=headersAPI)
    return(resp)

def getProjects(headersAPI, url=None, account_id=None) :
    """Get a list of projects
    The account_id is used in CPDaaS only
    """
    if url == None :
        url = WATSON_DATA_ENDPOINT + "/"
    if 'cpdaas-include-permissions' not in headersAPI :
            headersAPI['cpdaas-include-permissions'] = "true"
    limit = 100 # maximum number of return values. Default 10
    projects_json = []
    projects = "v2/projects?include=everything&limit=100"
    if account_id is not None :
        projects = projects + "&bss_account_id={}".format(account_id)
        headersAPI['cpdaas-include-permissions'] = "true"
    loop=True
    first = True
    while loop :
        if first is True :
            resp = requests.get(url + projects, headers=headersAPI)
            first = False
        else :
            resp = requests.get("{}{}&bookmark={}".format(url, projects, resp_json['bookmark']), headers=headersAPI)
        if resp.status_code > 202 : # if error
            print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
        resp_json = resp.json()
        if (resp_json['total_results'] == 0) :
            loop = False
        else :
            projects_json.extend(resp_json['resources'])
    return(projects_json)

def getProjectMembers(headersAPI, url, id):
    if 'cpdaas-include-permissions' not in headersAPI :
        headersAPI['cpdaas-include-permissions'] = "true"
    resp = requests.get(url + 'v2/projects/{}/members'.format(id),
                        headers=headersAPI)
    return resp

def addUserToProject(headersAPI, user_email, iam_id, project_id, role="editor"):
    data = {
        "members": [{
            "role": role,
            "state": "ACTIVE",  # default "ACTIVE"
            "id": iam_id,
            "user_name": user_email
        }]
    }
    if 'cpdaas-include-permissions' not in headersAPI :
        headersAPI['cpdaas-include-permissions'] = "true"
    resp = requests.post(WATSON_DATA_ENDPOINT + '/v2/projects/{}/members'.format(project_id),
                         json=data, headers=headersAPI)
    return(resp)

def addWMLToProject(headersAPI,project_id, ml) :
    compute = [{
        'type': "machine_learning", # From doc 
        'guid': ml['guid'],
        'name': ml['name'],
        'credentials': {},
        'crn': ml['crn'] # optional
    }]
    payload = {
        'compute': compute
    }
    if 'cpdaas-include-permissions' not in headersAPI :
        headersAPI['cpdaas-include-permissions'] = "true"
    resp = requests.patch(WATSON_DATA_ENDPOINT + '/v2/projects/{}'.format(project_id), 
                      json=payload, headers=headersAPI)
    return(resp)

def deleteProjectMember(headersAPI, prj_id, email) :
    if 'cpdaas-include-permissions' not in headersAPI :
        headersAPI['cpdaas-include-permissions'] = "true"
    resp = requests.delete(WATSON_DATA_ENDPOINT + '/v2/projects/{}/members/{}'.format(prj_id, email),
                        headers=headersAPI)
    if resp.status_code > 204 : # if error
            print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
    return resp

def cre8Project(headersAPI, project_desc, url=None):
    payload = {
        "name": project_desc["name"],
        "generator": project_desc["generator"],
        "storage": {
            "type": project_desc['storage']['type'],
            "guid": project_desc['storage']['guid'],
            "delegated": False  # default
        },
        "description": project_desc["description"],
        "public": False,  # default
        "tags": ["project"],
        "enforce_members": True,
        "tools": ["jupyter_notebooks", "spss_modeler",
                  "experiments", "data_refinery"]
    }
    if project_desc['storage']['resource_key_crn'] is not None :
        payload['storage']['resource_crn'] = project_desc['storage']['resource_key_crn']
    if url is None :
        url = WATSON_DATA_ENDPOINT
    if url[-1] != "/" :
        url = url + "/"
    endpoint = url + 'transactional/v2/projects'
    resp = requests.post(endpoint, json=payload, headers=headersAPI)
    if resp.status_code > 204:
        print("create_project: Status code: {}, reason: {}".format(
            resp.status_code, resp.reason))
        print(payload)
        print(resp.text)
    if resp.status_code > 220:
        project_id = None
    else:
        resp_json = resp.json()
        project_id = resp_json['location'].split('/')[-1]
        # print(json.dumps(resp_json, indent=2, sort_keys=False))
    return(project_id)

def deleteProject(headersAPI, url=None, id=None) :
    if url == None :
        url = WATSON_DATA_ENDPOINT + "/"
    if 'cpdaas-include-permissions' not in headersAPI :
        headersAPI['cpdaas-include-permissions'] = "true"
    resp = requests.delete(url + 'transactional/v2/projects/{}'.format(id),
                        headers=headersAPI)
    return resp

