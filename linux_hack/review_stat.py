#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Show status of reviews for a given change.
'''

import argparse
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
        wrapped_line += ' ' + word
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('commit', metavar='<commit>',
                        help='commit of the change')
    parser.add_argument('--linux_dir', metavar='<dir>', default='./',
                        help='path to linux repo')
    args = parser.parse_args()

    git_cmd = ['git', '-C', args.linux_dir]
    touching_files = subprocess.check_output(
            git_cmd + ['show', args.commit, '--pretty=', '--name-only']
            ).decode().strip().splitlines()

    subsys_maintainers = maintainers.parse_maintainers(
            os.path.join(args.linux_dir, 'MAINTAINERS'))
    subsys_of_change = {}
    for name, info in subsys_maintainers.items():
        for touching_file in touching_files:
            if file_is_for_subsystem(touching_file, info):
                subsys_of_change[name] = info
    print('subsystems of the change:')
    for name in subsys_of_change.keys():
        print('- %s' % name)

    log_output_sentences = subprocess.check_output(
            git_cmd + ['log', '-1', args.commit, '--pretty=%an <%ae>%n%n%B']
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

    max_cols = int(os.get_terminal_size().columns * 0.9)
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

if __name__ == '__main__':
    main()
