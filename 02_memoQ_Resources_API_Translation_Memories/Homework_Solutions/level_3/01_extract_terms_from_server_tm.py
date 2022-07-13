# *** LEVEL 2 - ADD TMX DATA TO SERVER TM
# The MemoQ resource API allows us to add new translation units to an existing translation memory
# We will use this knowledge to automate adding our local tmx files to a server tm!

import itertools
import re
import spacy
import os

from lxml import etree
from memoq import get_auth_token, get_tm, get_tus

sample_guid = '61359674-9c32-49b6-bb2b-c84b587e0d09'
os.environ["https_proxy"] = "http://cloudproxy.dhl.com:10123"


# TASK 1
# We saw a few ways that we can use the MemoQ resource API to automate tm processing
# However, we can also use it for more complext NLP processes!
# Write a function "extract_terms_from_memoq_tm"
# The function should accept one positional argument:
# - tm_guid: str, guid of the tm that a tmx should be added to
# The function should first acquire information about the tm and get source and target language
# From those languages it should create spacey nlp object
# It should then get all tus in the specific tm and iterate over them
# From there it can get source and target of each tu and use spacy to check each token
# If the token is a named entity, it should be added to a list of term candidates
# The function should then return this list of candidates
# You might want to consider writing a helper function that loads the correct spacy language model
# Remember that spacy language packages are not consistently names. This applies to German packages in particular!

def load_nlp(lang, model_size='lg'):
    if lang in ['de']:
        nlp = spacy.load(f'{lang}_core_news_{model_size}')
    else:
        nlp = spacy.load(f'{lang}_core_web_{model_size}')
    return nlp


def extract_terms_from_memoq_tm(tm_guid):
    term_candidates = set()
    lang_map = {'eng-US': 'en', 'ger-DE': 'de'}
    tm = get_tm(tm_guid)
    src_lang = lang_map[tm.get('SourceLangCode')]
    trg_lang = lang_map[tm.get('TargetLangCode')]
    src_nlp = load_nlp(src_lang)
    trg_nlp = load_nlp(trg_lang)
    tus = get_tus(tm_guid)
    for tu_data in tus:
        src_seg = tu_data.get('SourceSegment', '')
        src_seg = re.sub(r'<seg>(.+?)<\/seg>', r'\g<1>', src_seg)
        trg_seg = tu_data.get('TargetSegment', '')
        trg_seg = re.sub(r'<seg>(.+?)<\/seg>', r'\g<1>', trg_seg)
        src_doc = src_nlp(src_seg)
        trg_doc = trg_nlp(trg_seg)
        # Using itertools here is not necessary but a neat trick to reduce redundant code
        # This logic first loops over source, then over target tokens one after the other
        # Since the exact same thing happens to both we don't have to write it twice.
        for token in itertools.chain(src_doc, trg_doc):
            if token.ent_type_:
                term_candidates.add(token)
    return term_candidates


# TASK 2
# Test your function! Use the function "extract_terms_from_memoq_tm"
# Print out the results!

term_candidates = extract_terms_from_memoq_tm(sample_guid)
print(term_candidates)
