from __future__ import print_function

import json
import logging
import os
import sys

import requests

CONTRIBUTORS_URL = 'http://staging-api.osf.io/v2/nodes/{}/contributors/'
TOKEN = os.environ['TOKEN']

def get_contribs(url):
    contributors_to_add = []
    resp = requests.get(url).json()
    contributors = resp['data']

    for contrib in contributors:
        contributors_to_add.append(contrib['embeds']['users']['data']['id'])

    next_url = resp['links']['next']
    if next_url:
        contributors_to_add += get_contribs(next_url)
    return contributors_to_add


def add_contrib(url, uid, permission='read'):
    payload = {
        'data': {
            'type': 'contributors',
            'attributes': {
                'bibliographic': True,
                'permission': permission
            },
            'relationships': {
                'user': {
                    'data': {
                        'type': 'users',
                        'id': uid
                    }
                }
            }
        }
    }
    return requests.post(
        url,
        data=json.dumps(payload),
        headers={
            'Authorization': 'Bearer {}'.format(TOKEN),
            'Content-Type': 'application/json'
        })


def lambda_handler(event, context):
    to_proj = event['to']
    from_proj = event['from']
    url = CONTRIBUTORS_URL.format(from_proj)
    to_add = get_contribs(url)
    print(to_add)

    count = 0
    url = CONTRIBUTORS_URL.format(to_proj)
    for contrib in to_add:
        resp = add_contrib(url, contrib)
        print(resp)
        print(resp.status_code)
        count += 1 if resp.status_code == 201 else 0

    return 'Done with {} total contributors migrated'.format(count)
