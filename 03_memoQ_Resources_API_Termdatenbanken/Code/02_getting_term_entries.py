# *** MEMOQ RESOURCE API - GETTING TERM ENTRY INFORMATION *** #
# Using the memoQ Resource API to acquire entries in a termbase




import requests
import json
import os

from memoq import get_auth_token, get_tb

# os.environ["https_proxy"] = "http://cloudproxy.dhl.com:10123"


guid = '23a0a058-143c-404d-b3f7-60bf8b87d136'


# *** TERMINOLOGY LOOKUP *** #
# Finding terms in a termbase and filtering them by metadata values

def tb_lookup(guid, search_term, lang='eng', limit=100, term_condition="equals", md_condition="equals", client=None,
              domain=None, project=None, subject=None):
    """
    Finds entries in a TB that contain a term in a certain language
    :param guid: guid of the TB
    :param search_term: term to find entries for
    :param lang: language of the search term
    :param limit: how many results to return, default 100
    :param term_condition: Condition to search the term by. Supported: startswith, contains, endswith, equals
    :param md_condition: Condition to search metadata by. Supported: startswith, contains, equals, filled, not_equal,
    not_filled
    :param client: str, client value to filter results by. If None, no client filter is applied
    :param domain: str, domain value to filter results by. If None, no domain filter is applied
    :param project: str, project value to filter results by. If None, no project filter is applied
    :param subject: str, subject value to filter results by. If None, no subject filter is applied
    :return:
    """
    term_condition_map = {"startswith": 0, "contains": 1, "endswith": 2, "equals": 3}
    md_condition_map = {"startswith": 0, "contains": 1, "equals": 2, "filled": 3, "not_equal": 4, "not_filled": 5}
    term_condition = term_condition_map.get(term_condition, 3)
    md_condition = md_condition_map.get(md_condition, 2)
    request_data = {
      "FilteringConditions": [],
      "Limit": limit,
      "SearchExpression": search_term,
      "Condition": term_condition,
      "TargetLanguage": lang
    }
    if client:
        request_data["FilteringConditions"].append({"Condition": md_condition, "MetaName": 0, "MetaValue": client})
    if domain:
        request_data["FilteringConditions"].append({"Condition": md_condition, "MetaName": 1, "MetaValue": domain})
    if project:
        request_data["FilteringConditions"].append({"Condition": md_condition, "MetaName": 2, "MetaValue": project})
    if subject:
        request_data["FilteringConditions"].append({"Condition": md_condition, "MetaName": 3, "MetaValue": subject})
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/search?authToken={token}'
    tb_entries = requests.post(endpoint_url, data=request_data)
    return tb_entries.json()


# tb_entries = tb_lookup(guid, 'parcel', lang='eng', term_condition="startswith")
# print(json.dumps(tb_entries, indent=2))
# print(f'Found {len(tb_entries)} entries in TB!')


# *** GET TB ENTRY BY ID *** #
# Displaying individual entries in a TB using the MemoQ Resource API

def get_tb_entry(guid, entry_id):
    """
    Returns a single tb entry from the memoQ Resource API
    :return: all entries in a TB
    :rtype: list
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/{entry_id}/?authToken={token}'
    return requests.get(endpoint_url).json()


# tb_entries = get_tb_entry(guid, 21)
# print(json.dumps(tb_entries, indent=2))


# *** LIST TB ENTRIES *** #
# Displaying a list of entries in a TB using the MemoQ Resource API

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
    print(entry_num)
    if not entry_num:
        return tb_entries
    entries_found = 0
    entry_id = 0
    while entries_found < entry_num:
        entry_id += 1
        endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/{entry_id}/?authToken={token}'
        tb_entry = requests.get(endpoint_url).json()
        print(tb_entry)
        if not tb_entry.get('Id'):
            continue
        tb_entries.append(tb_entry)
        entries_found += 1
    return tb_entries


tb_entries = list_tb_entries(guid)
print(json.dumps(tb_entries, indent=2))
print(f'Found {len(tb_entries)} entries in TB!')


# *** FILTER TB ENTRIES *** #
# Filtering TB entries by entry, language or term level metadata

def filter_tb_entries(guid, client=None, domain=None, project=None, subject=None, custom_md=dict()):
    """
    Returns a list of tb entries from the memoQ Resource API filtered by entry metadata
    :param guid: guid of the TB
    :return: all entries in a TB
    :rtype: list
    """
    filtered_entries = list()
    tb_entries = list_tb_entries(guid)
    for tb_entry in tb_entries:
        skip_entry = False
        if client and tb_entry.get('Client') != client:
            skip_entry = True
        if project and tb_entry.get('Project') != project:
            skip_entry = True
        if domain and tb_entry.get('Domain') != domain:
            skip_entry = True
        if subject and tb_entry.get('Subject') != subject:
            skip_entry = True
        for custom_md_name, custom_md_value in custom_md.items():
            for entry_md in tb_entry.get('CustomMetas', list()):
                if entry_md.get("Name") != custom_md_name or entry_md.get("Value") != custom_md_value:
                    skip_entry = True
        if not skip_entry:
            filtered_entries.append(tb_entry)
    return filtered_entries


# tb_entries = filter_tb_entries(guid, subject='Vehicles')
# print(json.dumps(tb_entries, indent=2))
# print(f'Found {len(tb_entries)} entries in TB!')


# *** FINDING TERMS IN TRANSLATION MEMORIES *** #
# Finding terms in a TB in translation memory segments

# TODO: Knowing how to both get TUs and TB entries, we can now combine the two!
# TODO: Write a function "find_terms_in_tm" that identifies TUs in a TM that contain any term in a TB!
# TODO: The function should accept three positional argument:
# TODO: - tb_guid: str, guid of the TB with terms to check for
# TODO: - tm_guid: str, guid of the TM with tus to check
# TODO: The function should get all the terms in the tb and store them in a list
# TODO: Then iterate over all the TUs in a TM and add any to a result list, that contains a term
# TODO: The function should then return the list of results!

from memoq import get_tus


def find_terms_in_tm(tb_guid, tm_guid):
    """
    Finds TUs in a memoQ server TM that contain any term in a memoQ server TB
    :param tb_guid: str, guid of the TB to get terms from
    :param tm_guid: str, guid of the TM to search for terms
    :return: a list of json data for each TU that terms were found in
    :rtype: list
    """
    tus_w_terms = list()
    tb_terms = []

    tb_entries = list_tb_entries(tb_guid)
    for term in tb_entries:
        for lang in term["Languages"]:
            for items in lang["TermItems"]:
                term_texts = items["Text"]
                tb_terms.append(term_texts)
    tu_entries = get_tus(tm_guid)
    for src_trg in tu_entries:
        src_text = src_trg["SourceSegment"]
        for s in tb_terms:
            if s in src_text:
                tus_w_terms.append(s)
        trg_text = src_trg["TargetSegment"]
        for t in tb_terms:
            if t in trg_text:
                tus_w_terms.append(t)
    return tus_w_terms

tb_guid = '23a0a058-143c-404d-b3f7-60bf8b87d136'
tm_guid = '61359674-9c32-49b6-bb2b-c84b587e0d09'

found_tus = find_terms_in_tm(guid, tm_guid)

print(json.dumps(found_tus, indent=2))
