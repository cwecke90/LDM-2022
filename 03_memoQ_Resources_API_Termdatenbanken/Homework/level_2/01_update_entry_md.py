# *** LEVEL 2 - UPDATING ENTRY METADATA
# We learned how to filter entries by their metadata values, but what if we want to change existing metadata?
# We can combine some of the logic we have to automatically change metadata field values!

import requests
import json
import spacy

from memoq import get_auth_token, list_tb_entries, list_tbs

tb_guid = ''


# TASK 1
# Write a function "update_entry_metadata" that updates metadata in a termbase based on it's value
# It will find all metadata fields with certain values and substitute them with new values!
# The function should accept three positional argument:
# - tb_guid: str, guid of the termbase where metadata should be replaced
# - field_name: str, name of the metadata field to replace values in
# - old_value: str, old metadata value that should be replaced
# - new_value: str, new metadata value that should be inserted
# first, get all entries in the termbase with the guid you're passing to the function
# then iterate over all entries and check, if "field_name" is in the entry and if its value equals "old_value"
# if it does, replace it with "new_value"
# mind that you'll have to approach custom metadata values differently!
# after you have modified the dictionary, use the memoQ API to update the entry with the changed data
# The function should not return anything

def update_entry_metadata(tb_guid, field_name, old_value, new_value):
    """
    Updates metadata in memoQ termbase entries if they match a certain value.
    :param tb_guid: str, guid of the termbase where entries should be changed
    :param field_name: str, name of the metadata field where values should be changed
    :param old_value: str, metadata value that should be changed
    :param new_value: str, metadata value that will be inserted
    :return: None
    """
    pass


# TASK 2
# Test your function! Use the function "update_entry_metadata" to change entry metadata values
# In the default field "Domain" change the value "Logistics" to "Logistic engineering"
# In the custom field "Note" change the value "Entry for DPDHL" to "Entry for DPDHL group"

update_entry_metadata(tb_guid, 'Domain', 'Logistics', 'Logistic engineering')
update_entry_metadata(tb_guid, 'Note', 'Entry for DPDHL', 'Entry for DPDHL group')
