# *** LEVEL 2 - ADD TMX DATA TO SERVER TM
# The MemoQ resource API allows us to add new translation units to an existing translation memory
# We will use this knowledge to automate adding our local tmx files to a server tm!

import os
import requests

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
    token = get_auth_token()
    tmx_tree = etree.parse(tmx_path)
    tu_trees = tmx_tree.xpath('body/tu')
    for tu_tree in tu_trees:
        tu_data = dict()
        tu_segs = tu_tree.xpath('tuv/seg')
        context_pre = tu_tree.find('prop[type="x-context-pre"]')
        context_post = tu_tree.find('prop[type="x-context-post"]')
        tu_data['SourceSegment'] = f'<seg>{tu_segs[0].text}</seg>'
        tu_data['TargetSegment'] = f'<seg>{tu_segs[-1].text}</seg>' if len(tu_segs) > 1 else None
        tu_data['PrecedingSegment'] = context_pre.text if context_pre else None
        tu_data['FollowingSegment'] = context_post.text if context_post else None
        endpoint_url = f'https://mimesis.memoq.com:9091/loctimizetrain/memoqserverhttpapi/v1/tms/{tm_guid}/entries/create?authToken={token}'
        requests.post(endpoint_url, data=tu_data)


# TASK 2
# Test your function! Use the function "add_tmx_to_server_tm"
# Add to your MemoQ server all tus in the file "sample_tmx"
# Use the functions we learned about in the course to get the number of tus in the server tm
# Print out the number of tus to verify your function works!

add_tmx_to_server_tm(sample_guid, sample_tmx)

tm = get_tm(sample_guid)
print(tm.get('NumEntries'))
