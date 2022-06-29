# *** LEVEL 2 - ADD TMX DATA TO SERVER TM
# The MemoQ resource API allows us to add new translation units to an existing translation memory
# We will use this knowledge to automate adding our local tmx files to a server tm!

import os
import requests
import regex as re

from lxml import etree
from memoq import get_auth_token, get_tm

sample_tmx = os.path.join('files', 'sample.tmx')
sample_guid = '61359674-9c32-49b6-bb2b-c84b587e0d09'


# TASK 1
# We already know how to add translation units to an existing translation memory
# But what if we have potentially hundreds of tmx files that we want to add via API?
# We can write a function that simplifies this process for us!
# Write a function "add_tmx_to_server_tm"
# The function should accept two positional arguments:
# - tm_guid: str, guid of the tm that a tmx should be added to
# - tmx_path: str, path of the tmx file that should be added
# The function should iterate over all tus in a tmx file and add them to a MemoQ Server TM
# Don't worry about all the metadata for now!
# In this exercise, focus on adding new tus with their source, target, previous context and following context
# Use the Guid of the server tm you acquired during the course

def add_tmx_to_server_tm(tm_guid, tmx_path):
    tmx_tree = etree.parse(tmx_path)
    translation_units = tmx_tree.xpath('.//tu')
    token = get_auth_token()
    for tus in translation_units:
        tu_data = dict()
        tu_segments = tus.xpath('.//seg')
        src_segment = tu_segments[0]
        src_segment_text = etree.tostring(src_segment, encoding='utf-8').decode()
        src_segment_text = re.sub("<seg([^>]?)+>(.+?)<\/seg>", "\g<2>", src_segment_text)
        src_segment_text = src_segment_text.strip()
        src_context_pre = tus.find('.//prop[@type="x-context-pre"]')
        src_context_post = tus.find('.//prop[@type="x-context-post"]')
        if src_context_pre is not None:
            src_context_pre_text = src_context_pre.text
            tu_data['PrecedingSegment'] = src_context_pre_text
        if src_context_post is not None:
            src_context_post_text = src_context_post.text
            tu_data['FollowingSegment'] = src_context_post_text
        trg_segment = tu_segments[1]
        trg_segment_text = etree.tostring(trg_segment, encoding='utf-8').decode()
        trg_segment_text = re.sub("<seg([^>]?)+>(.+?)<\/seg>", "\g<2>", trg_segment_text)
        trg_segment_text = trg_segment_text.strip()
        tu_data['SourceSegment'] = f"<seg>{src_segment_text}</seg>"
        tu_data['TargetSegment'] = f"<seg>{trg_segment_text}</seg>"
        endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/' \
                       f'entries/create?authToken={token}'
        requests.post(endpoint_url, data=tu_data)


# TASK 2
# Test your function! Use the function "add_tmx_to_server_tm"
# Add to your MemoQ server all tus in the file "sample_tmx"
# Use the functions we learned about in the course to get the number of tus in the server tm
# Print out the number of tus to verify your function works!

tm_data = get_tm(sample_guid)
tm_entries = tm_data.get('NumEntries', 0)

print(f'Before adding TU. There are currently {tm_entries} tus in the TM')


add_tmx_to_server_tm(sample_guid, sample_tmx)

tm_data = get_tm(sample_guid)
tm_entries = tm_data.get('NumEntries', 0)

print(f'After adding TU. There are currently {tm_entries} tus in the TM')


