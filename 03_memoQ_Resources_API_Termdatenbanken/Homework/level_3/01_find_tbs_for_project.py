# *** LEVEL 3 - FINDING TERMBASES FOR A NEW PROJECT
# Sometimes we have many termbases and large quantities of text that need to be translated
# We then need to figure out, what termbases should be used as a resource for the text
# We can partially automate this process using nlp techniques!

import os
import spacy

from memoq import get_auth_token, list_tb_entries, list_tbs

sample_path = os.path.join('files', 'sample.txt')
with open(sample_path, 'r') as file:
    sample_text = file.read()


# TASK 1
# Write a function "find_tbs_by_text", that finds all termbases that can be used for translating a text
# It compares the lemmas in a text to the terms in memoQ termbases and finds those tbs relevant for translation
# The function should accept one positional argument:
# - text: str, the text that should be compared to the server termbases
# The function should accept one keyworded argument:
# - lang: str, a two letter language code representing the language of "text", e.g. "en"
# To do this, the function should use spacy to lemmatize the text and create a set of normalized (.lower()) lemmas
# It should then iterate over all termbases on the server and get the entries of every termbase
# It should then iterate over the entries, all languages in every entry and all terms in every language
# Normalize the term, if the term can be found in the set of text lemmas, the tb name and guid are added to the results
# The function should return a dictionary with as keys and tb names as values like this:
# {'eda46967-44e9-4967-b1db-47b5f2910bcc': 'LDM_TB_EW', '23a0a058-143c-404d-b3f7-60bf8b87d136': 'LDM_TB_CW'}

def find_tbs_by_text(text, lang='en'):
    """
    Lemmatizes a text and finds all termbases on a memoQ server, that have terms also contained in the text. It then
    returns a dictionary with the guids and names of those termbases.
    :param text: str, the text to compare to existing termbases
    :param lang: str, two letter language code for the text language
    :return: a dictionary with guids as keys and tb names as values
    :rtype: dict
    """
    project_tbs = dict()
    return project_tbs


# TASK 2
# Test your function! Use the function "find_tbs_by_text" to find all termbases containing terms relevant for the text!
# Pass "sample_text" as an argument to your function, the language should be "en"

project_tbs = find_tbs_by_text(sample_text, 'en')
print(project_tbs)
