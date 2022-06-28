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
    pass
    # TODO: Write your code here! Feel free to delete this comment!


# TASK 2
# Test your function! Use the function "add_tmx_to_server_tm"
# Add to your MemoQ server all tus in the file "sample_tmx"
# Use the functions we learned about in the course to get the number of tus in the server tm
# Print out the number of tus to verify your function works!

# TODO: Write your code here! Feel free to delete this comment!
