import json
import config
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AuthExceptionHTTPError(requests.exceptions.HTTPError):
    '''HTTP error while making auth request'''
    pass

class AuthExceptionBadFormat(Exception):
    '''HTTP response from auth contains unexpected format'''
    pass

def get_racker_token(username, password, server='https://identity-internal.api.rackspacecloud.com' ):
    '''Returns a Racker token for the given username and password'''
    path = '/v2.0/tokens'
    payload = {
        "auth": {
            "RAX-AUTH:domain": {"name": "Rackspace"},
            "passwordCredentials": {
                "username": config.username,
                "password": config.SSO,
            },
        }
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    req = requests.post(server + path, data=json.dumps(payload),
                        headers=headers, verify=False)
    if req.status_code not in range(200, 300):
        raise AuthExceptionHTTPError
    data = req.json()
    try:
        return data.get("access").get("token")
    except AttributeError:
        raise AuthExceptionBadFormat

token= get_racker_token("username","password")
print token
