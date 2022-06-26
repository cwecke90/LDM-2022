# *** MEMOQ RESOURCE API AUTHENTICATION *** #
# Logging into the MemoQ Resource API, acquiring an authentication token and listing translation memories

import os
import requests
import json

# os.environ["https_proxy"] = "http://cloudproxy.dhl.com:10123"

# *** INTERPRETING ERROR CODES *** #
# Receiving an error code from an API call and interpreting it.

def test_memoq_api():
    """
    Makes a test request to the MemoQ resource API.
    :return: API response data
    :rtype: dict
    """
    endpoint_url = 'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms?authToken=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    tms = requests.get(endpoint_url)
    return tms.json()


print(test_memoq_api())


# *** TOKEN AUTHENTICATION *** #
# Logging in to MemoQ and receiving a token for further authentication

def get_auth_token():
    """
    Acquired an authentication token for the MemoQ resource API. Reuses old tokens if they are still valid.
    :return: MemoQ resource API authentication token.
    :rtype: str
    """
    authentication_endpoint = 'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/auth/login'
    with open(os.path.join('files', 'token.json')) as token_file:
        token = json.load(token_file).get('AccessToken')
    tm_endpoint = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms?authToken={token}'
    api_response = requests.get(tm_endpoint).json()
    if isinstance(api_response, dict): # isinstance checks if an object is of a specified type, here dict
        if api_response.get('ErrorCode') != 'InvalidOrExpiredToken':
            with open(os.path.join('files', 'auth.json')) as auth_file:
                auth_data = json.load(auth_file)
            auth_response = requests.post(authentication_endpoint, data=auth_data)
            token_data = auth_response.json()
            with open(os.path.join('files', 'token.json', 'w')) as token_file:
                json.dump(token_data, token_file)
            token = token_data.get('AccessToken')
    return token


print('Acquired authentication token:')
print(get_auth_token())
