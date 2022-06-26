# *** MEMOQ RESOURCE API TU DATA *** #
# We know that we can use the MemoQ resource API to add tus to an existing TM in MemoQ
# We can use this functionality to automate TM

import requests
import re

import pandas as pd
import numpy as np

from datetime import datetime

from memoq import get_auth_token
from memoq import get_tm

tm_guid = 'd47c4808-7e9c-4f97-b629-00daeb7efda1'


# *** LIST TUS IN A TM *** #
# Getting all tus within a certain tm

def get_tus(tm_guid):
    """
    Returns all tus in a specific MemoQ translation memory.
    :param tm_guid:
    :return:
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


tu_data = get_tus(tm_guid)

print('Acquired tus:')
print(tu_data)


# *** FILTER TUS IN A TM *** #
# Filtering all tus in a tm by metadata values

def filter_tus_by_metadata(tu_data, field_name, field_value):
    tus = list()
    for tu in tu_data:
        if field_name in tu:
            tu_field_value = tu.get(field_name)
        else:
            tu_field_value = [custom_value for custom_name, custom_value in tu['CustomMetas'].items() if custom_name
                              == field_name]
        if tu_field_value != field_value:
            continue
        tus.append(tu)
    return tus


tu_data = get_tus(tm_guid)
tus_filtered = filter_tus_by_metadata(tu_data, 'Domain', 'Logistics')

print(f"Filtered {len(tus_filtered)} of {len(tu_data)} tus:")
print(tus_filtered)


# *** GETTING SOURCE AND TARGET SEGMENTS *** #
# Getting source and target segments from tus

def get_tu_srcs(tu_data):
    src_segs = list()
    for tu in tu_data:
        src_seg = tu.get('SourceSegment')
        src_seg = re.sub(r'<seg>(.+?)<\/seg>', r'\g<1>', src_seg)
        src_segs.append(src_seg)
    return src_segs


def get_tu_trgs(tu_data):
    trg_segs = list()
    for tu in tu_data:
        trg_seg = tu.get('TargetSegment')
        trg_seg = re.sub(r'<seg>(.+?)<\/seg>', r'\g<1>', trg_seg)
        trg_segs.append(trg_seg)
    return trg_segs


tu_data = get_tus(tm_guid)
tu_src_segs = get_tu_srcs(tu_data)
tu_trg_segs = get_tu_trgs(tu_data)


print(f'Found {len(tu_src_segs)} source segments')
print(tu_src_segs)
print(f'Found {len(tu_src_segs)} target segments')
print(tu_trg_segs)


# *** SAVING TUS AS A XLSX FILE *** #
# Acquiring tu segments and metadata and saving them in a XLSX file

# TODO: You might want to read information from a set of translation units and save it to either a file or a database
# TODO: This could be useful for handing someone else the content of a translation memory for review!
# TODO: Write a function "save_tus_to_xlsx"
# TODO: The function should save all the TUs in a MemoQ TM to a XLSX file
# TODO: The column headers should be source, target and all metadata field names
# TODO: The function should accept one positional argument:
# TODO: - tm_guid: str, guid of the tm that duplicates should be removed from
# TODO: It should return nothing and save a new XLSX file with tu information to disk

def save_tus_to_xlsx(tm_guid):
    """
    Saves all translation units in a specific MemoQ translation memory to disk as a XLSX file.
    :param tm_guid: guid of a MemoQ TM
    :return: None
    """
    pass


save_tus_to_xlsx(tm_guid)


# *** ADD TUS TO A TM *** #
# Adding new translation units to a specific translation memory

def add_tu(tm_guid, source, target, client=str(), domain=str(), project=str(), subject=str(), custom_metadata=dict()):
    """
    Adds a new translation unit to a specific translation memory. MemoQ checks automatically, if a tu with the same
    source and target text already exists and skips it if it does.
    :param tm_guid: guid of a MemoQ TM
    :param source: str, source text of the new tu
    :param target: str, target text of the new tu
    :param client: str, client metadata value of the new tu
    :param domain: str, domain metadata value of the new tu
    :param project: str, project metadata value of the new tu
    :param subject: str, subject metadata value of the new tu
    :param custom_metadata: dict, custom metadata values for the new tu as a dictionary with the shape
    {"metadata_field_name": "metadata_field_value"}
    :return: None
    """
    tu_data = dict()
    tu_data['SourceSegment'] = f"<seg>{source}</seg>"
    tu_data['TargetSegment'] = f"<seg>{target}</seg>"
    tu_data['Client'] = f"{client}" if client else None # ternary operation
    tu_data['Domain'] = f"{domain}" if domain else None
    tu_data['Project'] = f"{project}" if project else None
    tu_data['Subject'] = f"{subject}" if subject else None
    if custom_metadata:
        tu_data["CustomMetas"] = list()
        for custom_name, custom_value in custom_metadata.items():
            tu_data["CustomMetas"].append({"Name": custom_name, "Value": custom_value})
    token = get_auth_token()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/create?authToken={token}'
    requests.post(endpoint_url, data=tu_data)


# tu_data = get_tus(tm_guid)
# print(f'Before addind TU. There are currently {len(tu_data)} tus in the TM')
#
# add_tu(tm_guid, 'This is a test', 'Dies ist ein test', domain='Training', project='LDM', custom_metadata={'x-document': 'test.txt'})
#
# tu_data = get_tus(tm_guid)
# print(tu_data[-1])
# print(f'After adding TU. There are currently {len(tu_data)} tus in the TM')


# *** DELETE TUS IN A TM *** #
# Deleting tus from a specific translation memory

def del_tus(tm_guid, entry_id):
    """
    Deletes a translation unit from a specific MemoQ translation memory.
    :param tm_guid: str, guid of a MemoQ TM
    :param entry_id: int, entry id of a TU
    :return: None
    """
    token = get_auth_token()
    tm_data = get_tm(tm_guid)
    tm_entries = tm_data.get('NumEntries', 0)
    if tm_entries < entry_id:
        print(f'Entry number {entry_id} not found in tm!')
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/{entry_id}/delete?authToken={token}'
    requests.post(endpoint_url)


# tu_data = get_tus(tm_guid)
# print(f'Before deleting TU. There are currently {len(tu_data)} tus in the TM')
#
# del_tus(tm_guid, len(tu_data))
#
# tu_data = get_tus(tm_guid)
# print(f'After deleting TU. There are currently {len(tu_data)} tus in the TM')


# *** UPDATE TUS IN A TM *** #
# Updating existing translation units to a specific translation memory

def update_tu_source(tm_guid, entry_id, src_text):
    """
    Updates the source segment of a translation unit in a specific MemoQ translation memory.
    :param tm_guid: str, guid of a MemoQ TM
    :param entry_id: int, entry id of a TU
    :param src_text: str, new source text of the tu
    :return: None
    """
    token = get_auth_token()
    tm_data = get_tm(tm_guid)
    tm_entries = tm_data.get('NumEntries', 0)
    if tm_entries < entry_id:
        print(f'Entry number {entry_id} not found in tm!')
    post_data = dict()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/{entry_id}?authToken={token}'
    tu = requests.get(endpoint_url).json()
    post_data['Modifier'] = tu.get('Modifier')
    post_data['Modified'] = tu.get('Modified')
    post_data['SourceSegment'] = f"<seg>{src_text}</seg>"
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/{entry_id}/update?authToken={token}'
    requests.post(endpoint_url, post_data)


def update_tu_target(tm_guid, entry_id, trg_text):
    """
    Updates the target segment of a translation unit in a specific MemoQ translation memory.
    :param tm_guid: str, guid of a MemoQ TM
    :param entry_id: int, entry id of a TU
    :param trg_text: str, new source text of the tu
    :return: None
    """
    token = get_auth_token()
    tm_data = get_tm(tm_guid)
    tm_entries = tm_data.get('NumEntries', 0)
    if tm_entries < entry_id:
        print(f'Entry number {entry_id} not found in tm!')
    post_data = dict()
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/{entry_id}?authToken={token}'
    tu = requests.get(endpoint_url).json()
    post_data['Modifier'] = tu.get('Modifier')
    post_data['Modified'] = tu.get('Modified')
    post_data['TargetSegment'] = f"<seg>{trg_text}</seg>"
    endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/{entry_id}/update?authToken={token}'
    requests.post(endpoint_url, post_data)


# tu_data = get_tus(tm_guid)
# print(tu_data[-1])
# print(f'Before updating TU source. Source text of the last TU is currently {tu_data[-1].get("SourceSegment")}')
#
# update_tu_source(tm_guid, len(tu_data)-1, 'New source')
#
# tu_data = get_tus(tm_guid)
# print(f'After updating TU source. Source text of the last TU is currently {tu_data[-1].get("SourceSegment")}')
#
# tu_data = get_tus(tm_guid)
# print(f'Before updating TU target. Target text of the last TU is currently {tu_data[-1].get("TargetSegment")}')
#
# update_tu_target(tm_guid, len(tu_data)-1, 'New target')
#
# tu_data = get_tus(tm_guid)
# print(f'After updating TU target. Target text of the last TU is currently {tu_data[-1].get("TargetSegment")}')
