import requests
import urllib.parse

from cpdalllibs.cpdlib.constants import *

def getUsers(headersAPI, url) :
    """Get a list of users"""
    users = "usermgmt/users?includeAll=true"

    resp = requests.get(url + USRMGMT + users, headers=headersAPI)
    return(resp)

def getUser(headersAPI, url, user_id) :
    """Get a specific user by id"""
    user = "usermgmt/user/{}".format(user_id)

    resp = requests.get(url + USRMGMT + user, headers=headersAPI)
    return(resp)

def getGroups(headersAPI, url) :
    """Get the groups defined in CPD"""
    groups="usermgmt/v2/groups"
    resp = requests.get(url + groups, headers=headersAPI)
    return(resp)

def getRoles(headersAPI, url) :
    """Get the roles defined in CPD"""
    role="roles?include_users_count=true&include_user_groups_count=true"
    resp = requests.get(url + USRMGMT + role, headers=headersAPI)
    return(resp)

def getConfig(headersAPI, url) :
    """Get CPD configuration information"""
    config="usermgmt/config?includeAll=true"
    resp = requests.get(url + USRMGMT + config, headers=headersAPI)
    return(resp)

def cre8Role(headersAPI, url, data) :
    """Create a role based on the data argument"""
    role = "role"
    resp = requests.post(url + USRMGMT + role, 
				json=data, headers=headersAPI)
    return(resp)

def cre8Group(headersAPI, url, data) :
    """Create a group based on the data argument"""
    group = "usermgmt/v2/groups"
    resp = requests.post(url + group, 
				json=data, headers=headersAPI)
    return(resp)

# grant access to user
def cre8User(headersAPI, url, data) :
    """Create a user based on the data argument"""
    user = "user?migrated=false"
    resp = requests.post(url + USRMGMT + user, 
				json=data, headers=headersAPI)
    return(resp)

def addUserToGroup(headersAPI, url, group_id, user_id):
    """Add a user to a group"""
    group="usermgmt/v2/groups/{}/members".format(group_id)
    uid = int(user_id)
    data = {
         "user_identifiers": [ uid ]
    }
    resp = requests.post(url + group,
            json=data, headers=headersAPI, verify=True)
    return(resp)

def addRoleToUser(headersAPI, url, username, data) :
    """Add a role to a user"""
    user = urllib.parse.quote("{}user/{}?add_roles=true".format(USRMGMT, username))
    resp = requests.put(url + user, json=data, headers=headersAPI)
    return(resp)

def deleteUser(headersAPI, url, username) :
    """Delete a user from CPD"""
    user = "user/" + username
    resp = requests.delete(url + USRMGMT + user, headers=headersAPI)
    return(resp)

def deleteGroup(headersAPI, url, group_id) :
    """Delete a group from CPD"""
    group = "usermgmt/v2/groups/{}".format(group_id)
    resp = requests.delete(url + group, headers=headersAPI)
    return(resp)

def deleteRole(headersAPI, url, role_id) :
    """Delete a group from CPD"""
    role = "{}role/{}".format(USRMGMT, role_id)
    resp = requests.delete(url + role, headers=headersAPI)
    return(resp)