# *** MEMOQ RESOURCE API - GETTING TERMBASE INFORMATION *** #
# Using the memoQ Resource API to acquire termbase level inforamtion

import os
import requests
import json

from datetime import datetime

from memoq import get_auth_token


# *** LIST TBS *** #
# Displaying a list of TBs using the MemoQ Resource API

def list_tbs():
    """
    Returns a list of termbases from the MemoQ resource API.
    :return: all available TBs on MemoQ
    :rtype: list
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs?authToken={token}'
    tbs = requests.get(endpoint_url)
    return tbs.json()


# tbs = list_tbs()
# print(json.dumps(tbs, indent=2))
# print(f'Found {len(tbs)} TBs on the server!')


# *** FILTER TBS *** #
# Displaying a list of TBs filtered by language or metadata using the MemoQ Resource API

def filter_tbs_by_lang(langs):
    """
    Returns a list of termbases from the MemoQ resource API filtered by languages.
    :param langs: list, languages to filter by
    :return: all available TBs on MemoQ filtered by language
    :rtype: list
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs?authToken={token}'
    lang_params = ''
    for lang_index in range(len(langs)):
        lang_params += f'&lang[{lang_index}]={langs[lang_index]}'
    tm = requests.get(endpoint_url + lang_params)
    return tm.json()


def filter_tbs_by_md(metadata):
    """
    Returns a list of termbases from the MemoQ resource API filtered by metadata.
    :param metadata: dict, dictionary with metadata fields as keys and metadata values as values
    :return: all available TBs on MemoQ filtered by metadata
    :rtype: list
    """
    filtered_tbs = list()
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs?authToken={token}'
    tbs = requests.get(endpoint_url)
    tbs = tbs.json()
    for tb in tbs:
        for md_field, md_value in metadata.items():
            if md_field not in tb:
                continue
            if tb[md_field] != md_value:
                continue
            filtered_tbs.append(tb)
    return filtered_tbs


# tbs = filter_tbs_by_lang(['zho-CN', 'hrv'])
# print(json.dumps(tbs, indent=2))
# print(f'Found {len(tbs)} TBs on the server!')
#
# tbs = filter_tbs_by_md({'Domain': 'testing'})
# print(json.dumps(tbs, indent=2))
# print(f'Found {len(tbs)} TBs on the server!')


# *** FILTERING TBS BY LAST USED DATA *** #
# Filtering termbases by the date they've last been used at to find deprecated termbases

# TODO: We can easily filter termbases by various metadata values, but what if we wan to compare metadata?
# TODO: For example, we can get all termbases that are older than a certain date to find possibly deprecated terms!
# TODO: Write a function "filter_tbs_by_last_used_date" that finds all termbases newer or older than a certain data.
# TODO: The function should accept three positional argument:
# TODO: - year: int, the to check for
# TODO: - month: int, the month to check for
# TODO: - day: int, the day ot check for
# TODO: The function should accept one positional arguments:
# TODO: - find_older: bool, default True. If argument is true, the TBs must be older than the given date
# TODO: You will have to create a datetime object from those parameters, then get the "LastUsed" value of every TB
# TODO: You can parse this value into another datetime object, then compare the two objects!

def filter_tbs_by_last_used_date(year, month, day, find_older=True):
    """
    Returns a list of termbases from the MemoQ resource API filtered by last usage date.
    :param year: int, last usage year
    :param month: int, last usage month
    :param day: int, last usage day
    :param find_older: bool, if True function only finds those TBs with last usage dates older than the parameters
    :return: all available TBs on MemoQ
    :rtype: list
    """
    filtered_tbs = list()
    return filtered_tbs


# tbs = filter_tbs_by_last_used_date(2022, 7, 1, find_older=False)
# print(json.dumps(tbs, indent=2))
# print(f'Found {len(tbs)} TBs on the server!')


# *** GET INDIVIDUAL TBS *** #
# Displaying a list of TBs using the MemoQ Resource API

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


guid = '23a0a058-143c-404d-b3f7-60bf8b87d136'
tbs = get_tb(guid)
print(json.dumps(tbs, indent=2))
