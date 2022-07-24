import os
import json
import requests

import pandas as pd
import numpy as np

from datetime import datetime


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


def get_tus(tm_guid):
    """
    Returns all tus in a specific MemoQ translation memory.
    :param tm_guid: str, guid of the TM to get TUs from
    :return: a list of JSON date for each TU
    :rtype: list
    """
    tus = list()
    token = get_auth_token()
    tm_data = get_tm(tm_guid)
    tm_name = tm_data.get('FriendlyName', '')
    tm_entries = tm_data.get('NumEntries', 0)
    if not tm_entries:
        print(f'No entries in TM {tm_name}!')
        return tus
    for entry_id in range(tm_entries):
        endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/{entry_id}?authToken={token}'
        tu = requests.get(endpoint_url)
        tus.append(tu.json())
    return tus


def get_tb(guid):
    """
    Returns a list of termbases from the MemoQ resource API.
    :param guid: str, guid of the TB
    :return: all available TBs on MemoQ
    :rtype: list
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs?tbGuid={guid}&authToken={token}'
    tb = requests.get(endpoint_url)
    return tb.json()


def get_tb_entry(guid, entry_id):
    """
    Returns a single tb entry from the memoQ Resource API
    :return: all entries in a TB
    :rtype: list
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/{entry_id}/?authToken={token}'
    return requests.get(endpoint_url).json()


def list_tb_entries(guid):
    """
    Returns a list of tb entries from the memoQ Resource API
    :param guid: guid of the TB
    :return: all entries in a TB
    :rtype: list
    """
    tb_entries = list()
    token = get_auth_token()
    tb = get_tb(guid)
    entry_num = tb.get('NumEntries', 0)
    if not entry_num:
        return tb_entries
    entries_found = 0
    entry_id = 0
    while entries_found < entry_num-1:
        endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/{entry_id}/?authToken={token}'
        entry_id += 1
        tb_entry = requests.get(endpoint_url).json()
        if tb_entry.get('Id') is None:
            continue
        tb_entries.append(tb_entry)
        entries_found += 1
    return tb_entries
