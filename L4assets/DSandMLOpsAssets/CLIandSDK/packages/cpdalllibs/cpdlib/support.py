import json
import requests
from cpdalllibs.cpdlib.constants import *

# Another method would be to use username and api_key
def getToken(admin, passwd, url) :
        """Get the access token required to interface with CPD"""
        headers = {
                'Accept': 'application/json',
                'Content-type': 'application/json'
	}
        data = {
                "username" : admin,
                "password" : passwd
        }
        resp = requests.post(url + IDENTAUTH,
                        data=json.dumps(data), headers=headers,
                        verify=True)
        return(resp)
