# *** LEVEL 2 - ADD TMX DATA TO SERVER TM
# The MemoQ resource API allows us to add new translation units to an existing translation memory
# We will use this knowledge to automate adding our local tmx files to a server tm!

import itertools
import re
import spacy

from lxml import etree
from memoq import get_auth_token, get_tm, get_tus

sample_guid = '61359674-9c32-49b6-bb2b-c84b587e0d09'


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
    if lang == "en":
        model_name = f"{lang}_core_web_{model_size}"
    else:
        model_name = f"{lang}_core_news_{model_size}"
    nlp = spacy.load(model_name)
    return nlp


def extract_terms_from_memoq_tm(tm_guid):
    term_candidates = set()
    lang_map = {'eng-US': 'en', 'ger-DE': 'de'}
    tm_data = get_tm(tm_guid)
    src_lang = tm_data.get("SourceLangCode")
    trg_lang = tm_data.get("TargetLangCode")
    nlp_obj_src = load_nlp(lang_map[src_lang])
    nlp_obj_trg = load_nlp(lang_map[trg_lang])
    tus = get_tus(tm_guid)
    for segments in tus:
        if "ErrorCode" not in segments:
            source_segment = segments.get("SourceSegment")
            source_segment = re.sub(r'<seg>(.+?)<\/seg>', r'\g<1>', source_segment)
            target_segment = segments.get("TargetSegment")
            target_segment = re.sub(r'<seg>(.+?)<\/seg>', r'\g<1>', target_segment)
            doc_src = nlp_obj_src(source_segment)
            for ne_src in doc_src:
                if ne_src.ent_type_:
                    term_candidates.add(ne_src.text)
            doc_trg = nlp_obj_trg(target_segment)
            for ne_trg in doc_trg:
                if ne_trg.ent_type_:
                    term_candidates.add(ne_trg.text)
    return term_candidates


# TASK 2
# Test your function! Use the function "extract_terms_from_memoq_tm"
# Print out the results!

print(extract_terms_from_memoq_tm(sample_guid))
