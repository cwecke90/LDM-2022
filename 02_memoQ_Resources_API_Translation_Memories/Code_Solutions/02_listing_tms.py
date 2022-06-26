# *** MEMOQ RESOURCE API TM DATA *** #
# Using the MemoQ resource api to display tms, filter them and extract information.

import requests

from memoq import get_auth_token


# *** DISPLAY TMS *** #
# Displaying a list of TMs or a single TM using the MemoQ Resource API

def list_tms():
    """
    Returns a list of translation memories from the MemoQ resource API.
    :return: all available TMs on MemoQ
    :rtype: list
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms?authToken={token}'
    tms = requests.get(endpoint_url)
    return tms.json()


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


# *** GET TM LANGUAGES *** #
# List the source and target languages for all TMs on a server

def get_tm_src_langs(tm_data):
    """
    Returns the source languages in a list of TMs
    :param tm_data: list of tms returned from the MemoQ resource API
    :return: a list of source languages in given TMs
    :rtype: list
    """
    src_langs = set()
    for tm in tm_data:
        src_lang = tm.get('SourceLangCode')
        src_langs.add(src_lang)
    return src_langs


def get_tm_trg_langs(tm_data):
    """
    Returns the target languages in a list of TMs
    :param tm_data: list, tms returned from the MemoQ resource API
    :return: list of target languages in given TMs
    :rtype: list
    """
    trg_langs = set()
    for tm in tm_data:
        trg_lang = tm.get('TargetLangCode')
        trg_langs.add(trg_lang)
    return trg_langs


tm_data = list_tms()
src_langs = get_tm_src_langs(tm_data)
trg_langs = get_tm_trg_langs(tm_data)

print(f"Found {len(tm_data)} total tms:")
print(tm_data)
print(f"Found {len(src_langs)} source languages in {len(tm_data)} TMs:")
print(src_langs)
print(f"Found {len(trg_langs)} target languages in {len(tm_data)} TMs:")
print(trg_langs)


# *** FILTER TMS BY METADATA *** #
# Extending the functionality of MemoQ Resource API to filter TMs by metadata values

def filter_tms_by_domain(tm_data, domain):
    """
    Filters a set of MemoQ translation memories by their domain value.
    :param tm_data: list, tms returned from the MemoQ resource API
    :param domain: str, a domain value that TMs should be filtered by
    :return: TMs filtered by their domain value
    :rtype: list
    """
    tms = list()
    for tm in tm_data:
        tm_domain = tm.get('Domain')
        if tm_domain != domain:
            continue
        tms.append(tm)
    return tms


tm_data = list_tms()
tm_domain = 'Training'
tms_filtered = filter_tms_by_domain(tm_data, tm_domain)

print(f"Filtered {len(tms_filtered)} of {len(tm_data)} TMs:")
print(tms_filtered)


# *** EXTRACTING TM GUIDS *** #
# Getting specific guids from a list of tms

# TODO: Normally we don't want to process all the TMs on a MemoQ server
# TODO: But to access individual TMs, we need to use their respective guid
# TODO: The guid ID of each tm can be found in the data returned by the API much like languages and metadata!
# TODO: Write a function "get_guid_by_tm_name"
# TODO: The function should extract the guids of a list of tms whose names match a given string
# TODO: The function should accept one positional argument:
# TODO: - tm_data: json response containing tm data
# TODO: The function should accept two positional arguments:
# TODO: - name_start: string, name of the tm must start with this value unless the value is empty
# TODO: - name_end: string, name of the tm must end with this value unless the value is empty
# TODO: It should return a dictionary with found tm Guids as keys and their respective TM names as values
# TODO: Use the function to find out the guid of the TM whose names starts with "LDM" and ends with your initials!
# TODO: e.g. The TM for "Eric Wilke" would be "LDM_en-US_de-DE_EW"


def get_guid_by_tm_name(tm_data, name_start='', name_end=''):
    """
    Extracts the guids from a given set of MemoQ translation memories by their name.
    :param tm_data: list, tms returned from the MemoQ resource API
    :param name_start: str, sequence of characters, that the start of the TM name must match
    :param name_end: str, sequence of characters, that the end of the TM name must match
    :return: TMs filtered by their name
    """
    tms = dict()
    for tm in tm_data:
        tm_name = tm.get('FriendlyName', '')
        if name_start and not tm_name.startswith(name_start):
            continue
        if name_end and not tm_name.endswith(name_end):
            continue
        tm_guid = tm.get('TMGuid', '')
        tms[tm_guid] = tm_name

    return tms


tm_data = list_tms()
print(get_guid_by_tm_name(tm_data, name_end='_EW'))
