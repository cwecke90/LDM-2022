import os
import json
import requests


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
    if isinstance(api_response, dict):
        if api_response.get('ErrorCode') == 'InvalidOrExpiredToken':
            with open(os.path.join('files', 'auth.json')) as auth_file:
                auth_data = json.load(auth_file)
            auth_response = requests.post(authentication_endpoint, data=auth_data)
            token_data = auth_response.json()
            with open(os.path.join('files', 'token.json'), 'w') as token_file:
                json.dump(token_data, token_file)
            token = token_data.get('AccessToken')
    return token


def get_tm(tm_guid):
    """
    Returns a single translation memory from the MemoQ resource API by its guid.
    :return: A specific MemoQ TM
    :rtype: dict
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}?authToken={token}'
    tm = requests.get(endpoint_url)
    return tm.json()
