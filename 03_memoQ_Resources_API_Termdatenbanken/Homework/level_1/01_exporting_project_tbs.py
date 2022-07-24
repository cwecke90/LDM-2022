# *** LEVEL 1 - EXPORTING PROJECT TERMBASES
# We already developed a logic, that allows us to export and save our termbases
# To automate this further, we can use what we learned to export all termbases that are currently in use!

import requests

from memoq import export_tb_entries_xlsx, list_tbs


# TASK 1
# Write a function "export_used_termbases", that exports all termbases that are used in any project as XLSX files
# The function should accept one positional argument:
# - token: str, authentication token for the Smart Language Portal API
# To do this you will have to check the termbase metadata field "IsUsedInProject"
# If its value is True, get the termbase guid and export it
# Also check, if the name of the termbase starts with "LDM" to make sure we're only getting our own termbases
# You may reuse the function we've already written, add them to memoq.py and then import them here!
# The function should not return anything

def export_used_termbases():
    """
    Exports every termbase that is being used in a project and saves it as a new timestamped XLSX file.
    :return: None
    """
    pass


# TASK 2
# Test your function! Use the function "export_used_termbases" to export all termbases that are currently in use
# The output files will be saved in this directory

export_used_termbases()
