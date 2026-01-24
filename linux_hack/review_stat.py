#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Show status of reviews for given changes.

For flexible search of the data, '--output_format json' option can be used.
For example:

$ # save the data as a json file.
$ ./review_stat.py --commits mm-stable..mm-new --output_format json | tee foo
[...]
    {
        "change": "commit 27351535d7cd (\"mm/damon/paddr: initialize 'folio' variables to NULL for clarity\")",
        "subsystem_of_change": [
            "DAMON",
            "MEMORY MANAGEMENT",
            "THE REST"
        ],
        "tag_taggers": {
            "Link:": [
                "https://patch.msgid.link/20260104013255.16962-1-yangqixiao@inspur.com",
                "https://lkml.kernel.org/r/20260108013041.80601-1-sj@kernel.org"
            ],
            "Signed-off-by:": [
                "Aaron Yang <yangqixiao@inspur.com>",
                "SeongJae Park <sj@kernel.org>",
                "Andrew Morton <akpm@linux-foundation.org>"
            ],
            "Reviewed-by:": [
                "SeongJae Park <sj@kernel.org>"
            ]
        },
        "tagger_roles": {
            "https://patch.msgid.link/20260104013255.16962-1-yangqixiao@inspur.com": [],
            "https://lkml.kernel.org/r/20260108013041.80601-1-sj@kernel.org": [],
            "Aaron Yang <yangqixiao@inspur.com>": [
                "author"
            ],
            "SeongJae Park <sj@kernel.org>": [
                "DAMON maintainer"
            ],
            "Andrew Morton <akpm@linux-foundation.org>": [
                "MEMORY MANAGEMENT maintainer"
            ]
        }
    },
[...]
$
$ # load the data and find commits still waiting for reviews.
$ python3
>>> import json
>>> with open('foo', 'r') as f:
...		review_stats = json.load(f)
>>> for stat in review_stats:
...     if not 'Reviewed-by:' in stat['tag_taggers']:
...         print(stat['change'])
[...]
commit a73e1de6cdd2 ("mm/damon: update damos kerneldoc for stat field")
[...]
'''

import argparse
import json
import os
import subprocess

# imports of modules on same dir
import maintainers

def pr_wrapped(line, max_cols, first_line_prefix):
    words = line.split()
    indent_cols = len(first_line_prefix)
    wrapped_line = first_line_prefix
    for word in words:
        if len(wrapped_line) + 1 + len(word) > max_cols:
            print(wrapped_line)
            wrapped_line = indent_cols * ' '
        elif wrapped_line != '':
            wrapped_line += ' '
        wrapped_line += word
    print(wrapped_line)

def file_matching(file_tokens, path):
    path_tokens = path.split('/')
    if len(file_tokens) < len(path_tokens):
        return False

    path_is_dir = path[-1] == '/'
    for idx, file_token in enumerate(file_tokens):
        if path_is_dir is False and idx == len(path_tokens):
            return False
        if path_is_dir and idx == len(path_tokens) - 1:
            return True

        path_token = path_tokens[idx]
        if path_token == '*':
            continue
        if path_token != file_token:
            return False
    return True

def file_is_for_subsystem(file, subsys_maintainer_info):
    if not 'files' in subsys_maintainer_info:
        return False
    file_tokens = file.split('/')
    maintain_files = subsys_maintainer_info['files']
    for path in maintain_files:
        if file_matching(file_tokens, path):
            return True
    return False

def get_subsys_of_change(commit, linux_dir):
    git_cmd = ['git', '-C', linux_dir]

    touching_files = subprocess.check_output(
            git_cmd + ['show', commit, '--pretty=', '--name-only']
            ).decode().strip().splitlines()

    subsys_maintainers = maintainers.parse_maintainers(
            os.path.join(linux_dir, 'MAINTAINERS'))
    subsys_of_change = {}
    for name, info in subsys_maintainers.items():
        for touching_file in touching_files:
            if file_is_for_subsystem(touching_file, info):
                subsys_of_change[name] = info
    return subsys_of_change

def get_review_stat(commit, linux_dir):
    git_cmd = ['git', '-C', linux_dir]
    commit_desc = subprocess.check_output(
            git_cmd + ['log', commit, '-1',
                       '--pretty=commit %h ("%s")']).decode().strip()

    subsys_of_change = get_subsys_of_change(commit, linux_dir)

    log_output_sentences = subprocess.check_output(
            git_cmd + ['log', '-1', commit, '--pretty=%an <%ae>%n%n%B']
            ).decode().strip().split('\n\n')
    author = log_output_sentences[0]
    tag_taggers = {}
    tagger_roles = {}
    for line in log_output_sentences[-1].splitlines():
        fields = line.split()
        tag = fields[0]
        tagger = ' '.join(fields[1:])
        if not tagger in tagger_roles:
            tagger_roles[tagger] = []
        if not tag in tag_taggers:
            tag_taggers[tag] = []
        tag_taggers[tag].append(tagger)

    for tagger, roles in tagger_roles.items():
        if tagger == author:
            roles.append('author')
        for subsys_name, subsys_info in subsys_of_change.items():
            if 'maintainer' in subsys_info:
                if tagger in subsys_info['maintainer']:
                    roles.append('%s maintainer' % subsys_name)
            if 'reviewer' in subsys_info:
                if tagger in subsys_info['reviewer']:
                    roles.append('%s reviewer' % subsys_name)

    return commit_desc, subsys_of_change, tag_taggers, tagger_roles

def tagged_by(tag_taggers, subsys_of_change, tag, taggers):
    if not tag in tag_taggers:
        return False
    taggers_of_change = tag_taggers[tag]
    role_taggers = []
    for tagger in taggers:
        if tagger == 'anyone':
            return True
        if tagger in ['maintainer', 'reviewer']:
            role = tagger
            for name, info in subsys_of_change.items():
                if not role in info:
                    continue
                role_taggers += info[role]
    taggers += role_taggers
    for tagger in taggers:
        if tagger in taggers_of_change:
            return True
    return False

def skip_stat(subsys_of_change, tag_taggers, subsys_to_show,
              primary_signers_to_skip, signers_to_skip, reviewers_to_skip,
              ackers_to_skip):
    if subsys_to_show is not None:
        for subsys in subsys_to_show:
            if not subsys in subsys_of_change:
                return True
    if primary_signers_to_skip is not None:
        if 'Signed-off-by:' in tag_taggers:
            prime_tag_tagger = {'Signed-off-by:':
                                [tag_taggers['Signed-off-by:'][0]]}
            if tagged_by(prime_tag_tagger, subsys_of_change, 'Signed-off-by:',
                         primary_signers_to_skip):
                return True
    if signers_to_skip is not None and tagged_by(
            tag_taggers, subsys_of_change, 'Signed-off-by:', signers_to_skip):
        return True
    if reviewers_to_skip is not None and tagged_by(
            tag_taggers, subsys_of_change, 'Reviewed-by:', reviewers_to_skip):
        return True
    if ackers_to_skip is not None and tagged_by(
            tag_taggers, subsys_of_change, 'Acked-by:', ackers_to_skip):
        return True
    return False

def pr_review_stat(commit_desc, subsys_of_change, tag_taggers,
                       tagger_roles):
    try:
        max_cols = int(os.get_terminal_size().columns * 0.9)
    except OSError as e:
        # maybe redirecting the output.
        max_cols = 80
    pr_wrapped(commit_desc, max_cols, '')
    print('subsystems of the change:')
    for name in subsys_of_change.keys():
        print('- %s' % name)

    for tag, taggers in tag_taggers.items():
        print('%s' % tag)
        for tagger in taggers:
            roles = []
            if tagger in tagger_roles:
                roles = tagger_roles[tagger]
            if roles == []:
                pr_wrapped('%s' % tagger, max_cols, '- ')
            else:
                pr_wrapped('%s (%s)' % (tagger, ', '.join(roles)), max_cols,
                           '- ')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--commits', metavar='<commits>',
                        help='commits of the changes')
    parser.add_argument('--linux_dir', metavar='<dir>', default='./',
                        help='path to linux repo')
    parser.add_argument('--subsystem', metavar='<subsystem>', nargs='+',
                        help='subsystem of the change to show')
    parser.add_argument(
            '--not_primary_signed_off_by', metavar='<tagger>', nargs='+',
            help='skip commits signed off by given taggers')
    parser.add_argument('--not_signed_off_by', metavar='<tagger>', nargs='+',
                        help='skip commits signed off by given taggers')
    parser.add_argument('--not_reviewed_by', metavar='<tagger>', nargs='+',
                        help='skip commits reviewed by given taggers')
    parser.add_argument('--not_acked_by', metavar='<tagger>', nargs='+',
                        help='skip commits acked by given taggers')
    parser.add_argument('--drop_tag', nargs='+',
                        help='do not print specified tags')
    parser.add_argument(
            '--output_format', choices=['text', 'json', 'simpletext'],
            default='text',
            help='output format')
    args = parser.parse_args()

    if args.commits is None:
        print('--commits is essential')
        exit(1)

    json_data = []
    for commit in subprocess.check_output(
            ['git', '-C', args.linux_dir, 'log', '--pretty=%H', args.commits]
            ).decode().strip().splitlines():
        commit_desc, subsys_of_change, tag_taggers, tagger_roles = \
                get_review_stat(commit, args.linux_dir)
        if skip_stat(subsys_of_change, tag_taggers, args.subsystem,
                     args.not_primary_signed_off_by, args.not_signed_off_by,
                     args.not_reviewed_by, args.not_acked_by):
            continue
        if args.drop_tag is not None:
            for tag in args.drop_tag:
                del tag_taggers[tag]
        if args.output_format == 'text':
            pr_review_stat(commit_desc, subsys_of_change, tag_taggers,
                           tagger_roles)
            print()
        elif args.output_format == 'json':
            json_data.append({
                'change': commit_desc,
                'subsystem_of_change': list(subsys_of_change.keys()),
                'tag_taggers': tag_taggers,
                'tagger_roles': tagger_roles,
                })
        elif args.output_format == 'simpletext':
            print(commit_desc)
    if args.output_format == 'json':
        print(json.dumps(json_data, indent=4))

if __name__ == '__main__':
    main()
