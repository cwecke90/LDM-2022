# *** LEVEL 2 - ACCESS APIS
# We now know how to access and work with the data returned by the MemoQ resource API
# We should also remind ourselves, that we can transfer that knowledge to working with a variety of other API endpoints
# This will be useful in the future when we're working with machine translation services!
# For now, we will apply what we know to another API endpoint.
import json

import requests

slp_token = "dd65a4c333537f05c9abac96c04099338f0cde5c"


# TASK 1
# The Loctimize application Smart Language Portal also now has a functional API that can be accessed to acquire data
# Write a function "get_slp_langs"
# The function should call the Smart Language Portal API and get a list of available languages
# To do this, simply make GET request to the supplied endpoint
# The function should accept one positional argument:
# - token: str, authentication token for the Smart Language Portal API
# It should return a list of ISO-2 language codes
# Look closely at the returned JSON format and extract all appropriate language codes from it
# Mind that the Smart Language Portal API requires tokens to be passed in the request header!
# The header here is already given, you simply have to pass it to requests.get() as the appropriate argument

def get_slp_langs(token):
    locales = list()
    endpoint_url = 'https://example.dev.smart-language-portal.com/en/api/v1/portal/locales'
    header = {
        'Authorization': f'Token {token}',
        'accept': 'application/json'
    }
    response = requests.get(endpoint_url, headers=header)
    response_json = response.json()
    for lng in response_json["results"]:
        locales.append(lng["locale"])
    return locales


# TASK 2
# Test your function! Use the function "get_slp_langs" to acquire all available languages
# Then print the results out to the console

print(get_slp_langs(slp_token))


# TASK 3
# The Smart Language Portal locales API also supports different query parameters, that results can be filtered with
# One of those parameters is "active" which accepts either "true" or "false" as possible values
# If true, it will only return those languages that have been set as active by an administrator
# Languages that are not active will not be displayed in the UI while working on e.g. terminology
# Write a function "filter_slp_langs"
# The function should accept one positional argument:
# - token: str, authentication token for the Smart Language Portal API
# The function should accept one keyworded argument:
# - active: bool, if true only returns active languages, if false only returns languages that are not active
# It should return a list of ISO-2 language codes
# You can adjust your function "get_slp_langs" to achieve this!

def filter_slp_langs(token, active=True):
    locales = list()
    endpoint_url = 'https://example.dev.smart-language-portal.com/en/api/v1/portal/locales'
    header = {
        'Authorization': f'Token {token}',
        'accept': 'application/json'
    }
    response = requests.get(endpoint_url, headers=header)
    response_json = response.json()
    for lng in response_json["results"]:
        if lng["active"] == active:
            locales.append(lng["locale"])
    return locales


# TASK 4
# Test your function! Use the function "filter_slp_langs" to acquire all active and inactive languages!
# Then print the results out to the console

print(filter_slp_langs(slp_token))
