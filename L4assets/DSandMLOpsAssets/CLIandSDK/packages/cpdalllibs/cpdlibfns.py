import requests
from requests.structures import CaseInsensitiveDict
import json
from cpdalllibs.cpdlib.constants import *
from cpdalllibs.cpdlib.support   import *
from cpdalllibs.cpdlib.usermgmt  import *
from cpdalllibs.cpdlib.services  import *
from cpdalllibs.commonlib.projectmgmt import *

def importcpd() :
    return