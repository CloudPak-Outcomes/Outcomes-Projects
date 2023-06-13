import requests

from cpdalllibs.cpdaaslib.constants import *

def getUsers(headersAPI, account_id) :
    '''Get all the users that are part of the account'''
    all_users = []
    resp = requests.get(USER_MGMT_ENDPOINT + '/v2/accounts/{}/users'.format(account_id), headers=headersAPI)
    print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
    resp_json = resp.json()
    resp_json0 = resp_json
    #all_users = [ {'iam_id': name['iam_id'], 'user_id': name['user_id'], 'state': name['state']} for name in resp_json['resources']]
    all_users = [{k: name[k] for k in ('iam_id', 'user_id', 'state', 'added_on')} for name in resp_json['resources']]

    while ('next_url' in resp_json):
        resp = requests.get(USER_MGMT_ENDPOINT + resp_json['next_url'], headers=headersAPI)
        resp_json = resp.json()
        all_users = all_users + [{k: name[k] for k in ('iam_id', 'user_id', 'state', 'added_on')} for name in resp_json['resources']]
    return(all_users)

def inviteUser(headersAPI,account_id, data) :
    """Invite a user to an account"""
    url = USER_MGMT_ENDPOINT + '/v2/accounts/{}/users'.format(account_id)
    resp = requests.post(url, json=data, headers=headersAPI)
    return(resp)

def removeUser(headersAPI, iam_id, account_id) :
    """Remove a user from the account"""
    url = USER_MGMT_ENDPOINT + '/v2/accounts/{}/users/{}'.format(account_id,iam_id)
    resp = requests.delete(url, headers=headersAPI)
    return(resp)

def getAccessGroups(headersAPI, account_id) :
    """Get all access groups"""
    limit = 100 # max value: 100, default 20
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

def getGroupMembers(headersAPI, group_id) :
    """Get an access group members"""
    url = IAM_ENDPOINT + '/v2/groups/{}/members'.format(group_id)
    limit = 100 # max value: 100, default 20
    members_json = []
    resp = requests.get(url, headers=headersAPI)
    if resp.status_code > 202 : # if error
        print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
    else :
        resp_json = resp.json()
        members_json = resp_json['members']
        while 'next' in resp_json :
            resp = requests.get(resp_json['next']['href'], headers=headersAPI)
            resp_json = resp.json()
            members_json.extend(resp_json['members'])
    return members_json

def getGroupRules(headersAPI, group_id) :
    """Get the rules part of a group"""
    url = IAM_ENDPOINT + '/v2/groups/{}/rules'.format(group_id)
    resp = requests.get(url, headers=headersAPI)
    return(resp)


def cre8Group(headersAPI, account_id, group_name, group_description="") :
    """Create an access group"""
    data = {
        "name": group_name, 
        "description": group_description
    }
    url = IAM_ENDPOINT + '/v2/groups?account_id={}'.format(account_id)
    resp = requests.post(url, json=data, headers=headersAPI)
    return(resp)

def deleteGroup(headersAPI, group_id) :
    """Remove an access group from the account"""
    url = IAM_ENDPOINT + '/v2/groups/{}'.format(group_id)
    resp = requests.delete(url, headers=headersAPI)
    return(resp)

def getRoles(headersAPI) :
    '''Get the roles for the account'''
    resp = requests.get(IAM_ENDPOINT + '/v2/roles', headers=headersAPI)
    if resp.status_code > 202 : # if error
        print("Status code: {}, reason: {}".format(resp.status_code,resp.reason))
    return(resp.json())
