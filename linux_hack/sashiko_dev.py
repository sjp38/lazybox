#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
https://sashiko.dev provides AI review results of kernel patches.  Fetch the
results and show those on the terminal.
'''

import argparse
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('msgid', metavar='<msgid>',
                        help='message id of the patch')
    args = parser.parse_args()

    session = requests.session()
    session.headers.update({'User-Agent': 'lazybox'})
    resp = session.get('https://sashiko.dev/api/patch',
                       params={'id': args.msgid}, timeout=30)
    if resp.status_code != 200:
        print('get fail %s' % resp.status_code)
    data = resp.json()
    id_patch_map = {}
    for patch in data['patches']:
        id_patch_map[patch['id']] = patch

    for idx, review in enumerate(data['reviews']):
        print('review %d' % idx)
        print('result: %s' % review['result'])
        print('status: %s' % review['status'])
        patch_id = review['patch_id']
        patch = id_patch_map[patch_id]
        print('patch subject: %s' % patch['subject'])
        print('patch msgid: %s' % patch['message_id'])
        print('inline review')
        print(review['inline_review'])

if __name__ == '__main__':
    main()
