import requests
from cpdalllibs.commonlib.constants import *

def getAssetTypes(headersAPI, type, guid, url=None) :
    """Get asset types in project using a project id
    type is: catalog_id, project_id, space_id, or bss_account_id
    """
    if url is None :
        url = WATSON_DATA_ENDPOINT
    if url[-1] != "/" :
        url = url + "/"
    endpoint = url + 'v2/asset_types?{}={}'.format(type, guid)
    resp = requests.get(endpoint, headers=headersAPI)
    return(resp)

def getEnvironments(headersAPI, type, guid, url=None) :
    """Get environments in project using a project id
    type is: catalog_id, project_id, space_id, or bss_account_id
    """
    if url is None :
        url = WATSON_DATA_ENDPOINT
    if url[-1] != "/" :
        url = url + "/"
    endpoint = url + 'v2/environments?{}={}'.format(type, guid)
    resp = requests.get(endpoint, headers=headersAPI)
    return(resp)

def getContainer(headersAPI, type, guid, url=None) :
    """Get environments in project using a project id
    type is: catalog_id, project_id, space_id, or bss_account_id
    """
    if url is None :
        url = WATSON_DATA_ENDPOINT
    if url[-1] != "/" :
        url = url + "/"
    endpoint = url + 'v2/asset_containers/configurations?{}={}'.format(type, guid)
    resp = requests.get(endpoint, headers=headersAPI)
    return(resp)

def deleteProjectAsset(headersAPI, assetid, projectid, url) :
    """Mark an asset for deletion"""
    if url is None :
        url = WATSON_DATA_ENDPOINT
    if url[-1] != "/" :
        url = url + "/"
    endpoint = url + 'v2/assets/{}?project_id={}'.format(assetid, projectid)
    resp = requests.get(endpoint, headers=headersAPI)
    return(resp)