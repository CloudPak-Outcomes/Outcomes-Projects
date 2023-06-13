import json
import requests
from cpdalllibs.cpdlib.constants import *

### Undocumented API...
# This API was found on github
# https://github.com/IBM/watson-machine-learning-samples/blob/585613f07f968df1b1620ece283ec9d22b941d07/cpd4.5/notebooks/python_sdk/deployments/custom_software_spec/Use%20Custom%20Image%2C%20Software%20Specification%20and%20Runtime%20Definition%20to%20deploy%20a%20python%20function.ipynb#L496
def getServiceInstances(headersAPI, url) :
    '''Get all the services part of this cluster'''
    endpoint = url + '/zen-data/v3/service_instances?fetch_all_instances=true'
    resp = requests.get(endpoint, headers=headersAPI, verify=False)
    return resp

def getSvcToken(headersAPI, url, svc_id) :
    '''Get a token for a service'''
    endpoint = url + 'zen-data/v3/service_instances/{}/token'.format(svc_id)
    resp = requests.get(endpoint, headers=headersAPI, verify=False)
    return resp

def getSvcUsers(headersAPI, url, svc_id) :
    '''Get the users for a service'''
    endpoint = url + 'zen-data/v2/serviceInstance/users?sID={}'.format(svc_id)
    resp = requests.get(endpoint, headers=headersAPI, verify=False)
    return resp

def addSvcUser(headersAPI, url, data) :
    '''Add a user to a service'''
    endpoint = url + 'zen-data/v2/serviceInstance/users'
    resp = requests.post(endpoint, json=data, headers=headersAPI, verify=False)
    return resp

def deleteSvcUser(headersAPI, url, data) :
    '''Delete a member of a service'''
    endpoint = url + 'zen-data/v2/serviceInstance/users'
    resp = requests.delete(endpoint, json=data, headers=headersAPI, verify=False)
    return resp


# https://github.com/search?q=org%3AIBM%20v3%2Fservice_instances&type=code
# CP4D_INSTANCES_USERS=${CP4D_URL}/zen-data/v2/serviceInstance/users
# CP4D_INSTANCES_USERS_ROLE=${CP4D_INSTANCES_USERS}/role
# https://github.com/IBM/cloud-pak-deployer/blob/eb880b56439039163176b89c15716e37b1065184/automation-roles/60-configure-cloud-pak/cp4d/cp4d-instance-cognos/files/assign_CA_authorization.sh#L57

# export ADD_USER_TO_CA=$(curl -s -k -X POST -H "Authorization: Bearer ${BEARER}" -H 'Content-Type: application/json' ${CP4D_INSTANCES_USERS} \
#                   -d "{\"users\":[{\"uid\":\"${CP4D_USER_UID}\",\"username\":\"${LDAP_USER_NAME}\",\"display_name\":\"${LDAP_USER_DISPLAY_NAME}\",\"role\":\"${CP4D_CA_ROLE}\"}],\"serviceInstanceID\":\"${COGNOS_INSTANCE_ID}\"}" | jq -r '. | .message')
# export MODIFY_CA_ROLE=$(curl -s -k -X PATCH -H "Authorization: Bearer ${BEARER}" -H 'Content-Type: application/json' ${CP4D_INSTANCES_USERS_ROLE} \
#                   -d "{\"serviceInstanceID\":\"${COGNOS_INSTANCE_ID}\",\"roles\":[{\"uid\":\"${CP4D_USER_UID}\",\"newrole\":\"${CP4D_CA_ROLE}\"}]}" | jq -r '. | .message')
# export MODIFY_CA_ROLE=$(curl -s -k -X PATCH -H "Authorization: Bearer ${BEARER}" -H 'Content-Type: application/json' ${CP4D_INSTANCES_USERS_ROLE} \
#                   -d "{\"serviceInstanceID\":\"${COGNOS_INSTANCE_ID}\",\"roles\":[{\"uid\":\"${CP4D_USER_UID}\",\"newrole\":\"${CP4D_CA_ROLE}\"}]}" | jq -r '. | .message')

