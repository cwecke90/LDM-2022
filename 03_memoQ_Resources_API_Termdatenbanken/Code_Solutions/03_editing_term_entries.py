# *** MEMOQ RESOURCE API - EDITING TERM ENTRIES*** #
# Using the memoQ Resource API to acquire entries in a termbase


import requests
import json

from memoq import get_auth_token, get_tb, get_tb_entry, list_tb_entries


guid = 'eda46967-44e9-4967-b1db-47b5f2910bcc'


# *** ADD TB ENTRIES *** #
# Adding a new entry to an existing termbase

def add_tb_entry(guid, terms, client=None, domain=None, project=None, subject=None):
    """
    Adds a single entry to a memoQ server TB
    :param guid: guid of the TB
    :param terms: dict, dictionary with language codes as keys and lists of associated terms as values
    :param client: str, client value of the entry
    :param domain: str, domain value of the entry
    :param project: str, project value of the entry
    :param subject: str, subject value of the entry
    :return: None
    """
    entry_data = {"Client": client, "Domain": domain, "Project": project, "Subject": subject, "Languages": []}
    headers = {"Content-type": "application/json"}
    for lang, terms in terms.items():
        lang_data = {"Language": lang, "TermItems": []}
        for term in terms:
            term_data = {"Text": term}
            lang_data["TermItems"].append(term_data)
        entry_data["Languages"].append(lang_data)
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/create/?authToken={token}'
    requests.post(endpoint_url, data=json.dumps(entry_data), headers=headers)


# add_tb_entry(guid, {'ger': ['Gleisanlage'], 'eng': ['track system', 'trackage']}, client='DB', domain='Infrastructure')


# *** DELETE TB ENTRIES *** #
# Deleting existing entries from a termbase

def del_tb_entry(guid, entry_id):
    """
    deletes a single entry from a memoQ server TB
    :param guid: guid of the TB
    :param entry_id: id of the entry to delete
    :return: None
    """
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/{entry_id}/delete/?authToken={token}'
    requests.post(endpoint_url)


# entry_id = list_tb_entries(guid)[-1].get('Id')
# del_tb_entry(guid, entry_id)


# *** UPDATE TB ENTRIES *** #
# Update existing entries in a termbase

def edit_tb_entry_domain(guid, entry_id, domain):
    """
    Updates domain metadata value in a single TB entry from the memoQ Resource API
    :param guid: guid of the TB
    :param entry_id: id of the entry to update
    :param domain: str, domain value of the entry
    :return: None
    """
    entry_data = get_tb_entry(guid, entry_id)
    entry_data['Domain'] = domain
    token = get_auth_token()
    headers = {"Content-type": "application/json"}
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/{entry_id}/update/?authToken={token}'
    requests.post(endpoint_url, data=json.dumps(entry_data), headers=headers)


def edit_tb_entry_client(guid, entry_id, client):
    """
    Updates client metadata value in a single TB entry from the memoQ Resource API
    :param guid: guid of the TB
    :param entry_id: id of the entry to update
    :param client: str, client value of the entry
    :return: None
    """
    entry_data = get_tb_entry(guid, entry_id)
    entry_data['Client'] = client
    token = get_auth_token()
    headers = {"Content-type": "application/json"}
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/{entry_id}/update/?authToken={token}'
    requests.post(endpoint_url, data=json.dumps(entry_data), headers=headers)


# entry_id = get_tb(guid).get('NumEntries')
# edit_tb_entry_domain(guid, entry_id, 'Brand new domain')
# edit_tb_entry_client(guid, entry_id, 'Brand new client')
