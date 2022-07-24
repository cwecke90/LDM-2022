# *** MEMOQ RESOURCE API - EDITING TERM ENTRIES*** #
# Using the memoQ Resource API to write custom logic that exports and imports termbase entries

import os
import requests
import json
import copy

import pandas as pd
import numpy as np

from datetime import datetime

from memoq import get_auth_token, get_tb, get_tb_entry, list_tb_entries


guid = 'eda46967-44e9-4967-b1db-47b5f2910bcc'


# *** EXPORT TB ENTRIES *** #
# Exporting all entries in a memoQ server TB

def export_tb_entries_xlsx(guid):
    """
    Exports entries in a memoQ server TB as an XLSX file in qTerm multiline format
    :param guid: str, guid of the TB to export from
    :return: None
    """
    # We define three separate data frames for entry, language and term data
    # This is because we might have to add custom metadata column to them and those can have the same names
    tb_entry_df = pd.DataFrame(columns=[
        'Entry_ID', 'Entry_Subject', 'Entry_Domain', 'Entry_ClientID', 'Entry_ProjectID', 'Entry_Created',
        'Entry_Creator', 'Entry_LastModified', 'Entry_Modifier',
    ])
    tb_lang_df = pd.DataFrame(columns=[
        'Language_Definition', 'Language',
    ])
    tb_term_df = pd.DataFrame(columns=[
        'Term', 'Term_CaseSensitivity', 'Term_Forbidden', 'Term_PrefixMatching',
    ])
    tb_entries = list_tb_entries(guid)
    term_id = 0

    # We then nest three for loops:
    # one for all entries in a termbase, one for all languages in an entry, one for all terms in a language
    for entry in tb_entries:
        for lang in entry.get('Languages', list()):
            for term in lang.get('TermItems', list()):
                term_id += 1
                # Since we want to combine the data frames later, we have to make sure they are always the same size
                tb_entry_df.loc[term_id] = [np.nan for col_index in range(len(tb_entry_df.columns))]
                tb_lang_df.loc[term_id] = [np.nan for col_index in range(len(tb_lang_df.columns))]
                tb_term_df.loc[term_id] = [np.nan for col_index in range(len(tb_term_df.columns))]

                # Now we can start adding values to each data frame
                # This logic can be extended for every other conceivable metadata value
                tb_entry_df.at[term_id, 'Entry_ID'] = entry.get('Id')
                tb_lang_df.at[term_id, 'Language'] = lang.get('Language')
                tb_lang_df.at[term_id, 'Language_Definition'] = lang.get('Definition')
                tb_term_df.at[term_id, 'Term'] = term.get('Text')
                for custom_md in entry.get('CustomMetas', list()):
                    custom_field = custom_md.get('Name')
                    custom_value = custom_md.get('Value')
                    if custom_field not in tb_entry_df.columns:
                        tb_entry_df.insert(tb_entry_df.columns.get_loc('Entry_Modifier') + 1, custom_field, np.nan)
                    tb_entry_df.at[term_id, custom_field] = custom_value


    # We then get the name of the termbase and use it as the new file name
    tb_name = get_tb(guid).get('FriendlyName')
    tb_file_name = f"{tb_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
    tb_df = pd.concat([tb_entry_df, tb_lang_df, tb_term_df], axis=1)
    tb_df.to_excel(tb_file_name, index=False)


export_tb_entries_xlsx(guid)


# *** IMPORT TB ENTRIES *** #
# Importing entries from an xlsx file into a memoQ server TB

def import_tb_entries_xlsx(guid, path):
    """
    Imports entries from a qTerm multiline format XLSX file into a memoQ server TB
    :param guid: str, guid of the TB to import into
    :param path: str, path to the file that should be imported
    :return: None
    """
    # We store all entries in the XLSX file here and import them all later
    import_entries = list()

    # Then import the file as a data frame. Converting it to a dictionary makes iterations faster and access easier!
    tb_df = pd.read_excel(path)
    tb_df = tb_df.to_dict('records')

    tb_entry_template = {'Languages': [], 'CustomMetas': []}
    tb_lang_template = {'TermItems': [], 'CustomMetas': []}

    # We start with an entry ID and language that cannot normally exist in a termbase
    # That way our following condition that checks previous entry ID will always be true on the first iteration!
    prev_entry_id = -1
    prev_lang = -1
    for row in tb_df:
        entry_id = row['Entry_ID']

        # If we find a new entry and the current entry ID is not empty, we create a new dictionary
        if not pd.isnull(entry_id) and entry_id != prev_entry_id:
            # On the very first iteration, we don't want to add the entry dictionary to our results yet
            # We haven't added anything to it yet, it would just be empty!
            if prev_entry_id > -1:
                import_entries.append(tb_entry)
            tb_entry = copy.deepcopy(tb_entry_template)
            # tb_entry['Id'] = entry_id
            prev_entry_id = entry_id
            prev_lang = -1
        lang = row['Language']
        if not pd.isnull(lang) and lang != prev_lang:
            tb_lang = copy.deepcopy(tb_lang_template)
            tb_lang['Language'] = lang
            tb_entry['Languages'].append(tb_lang)
            prev_lang = lang
        # From here we can add terms or metadata
        tb_term = {'Text': row['Term'], 'CustomMetas': []}

        tb_lang['TermItems'].append(tb_term)
        custom_meta_level = 1

        # We can find custom metadata fields, by checking all field names that don't start with Entry, Language or Term
        for field_name in row:
            field_value = row[field_name]
            if pd.isnull(field_value):
                continue
            # If we arrive at 'Language' we know every following custom field is on language level!
            if field_name == 'Language':
                custom_meta_level = 2
            # If we arrive at 'Term' we know every following custom field is on term level!
            elif field_name == 'Term':
                custom_meta_level = 3
            elif not field_name.startswith(('Term_', 'Language_', 'Entry_')):
                if custom_meta_level == 1:
                    if not {field_name: field_value} in tb_entry['CustomMetas']:
                        tb_entry['CustomMetas'].append({'Name': field_name, 'Value': field_value})
                if custom_meta_level == 2:
                    if not {field_name: field_value} in tb_lang['CustomMetas']:
                        tb_lang['CustomMetas'].append({'Name': field_name, 'Value': field_value})
                if custom_meta_level == 3:
                    if not {field_name: field_value} in tb_term['CustomMetas']:
                        tb_term['CustomMetas'].append({'Name': field_name, 'Value': field_value})

    # The last entry will not be appended to the list of import entries with our previous logic
    # Therefore we have to append it, once the loop is finished
    import_entries.append(tb_entry)

    # Then we iterate over the entry data and add each to the termbase
    for entry in import_entries:
        token = get_auth_token()
        headers = {"Content-type": "application/json"}
        endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tbs/{guid}/entries/create/?authToken={token}'
        requests.post(endpoint_url, data=json.dumps(entry), headers=headers)


# tb_path = os.path.join('files', 'LDM_TB_Import.xlsx')
# import_tb_entries_xlsx(guid, tb_path)
