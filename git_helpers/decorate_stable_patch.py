#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('patch', metavar='<file>',
            help='patch file to add the upstream commit line')
    parser.add_argument('upstream_remote', metavar='<remote>',
            help='git remote name of the upstream')
    args = parser.parse_args()

    with open(args.patch, 'r') as f:
        patch_content = f.read()

    description_diff = patch_content.split('---\n')
    description = description_diff[0]
    author = None
    subject = None
    for line in description.split('\n'):
        if line.startswith('From: '):
            author = line.split('From: ')[1].strip()
        if line.startswith('Subject: [PATCH'):
            subject_fields = line.split(']')[1:]
            subject = ']'.join(subject_fields).strip()
    if author == None or subject == None:
        print('author and subject are not found')
        exit(1)

    if subject.startswith('resolve conflict'):
        with open(args.patch + '.new', 'w') as f:
            f.write(patch_content)
            exit(0)

    bindir = os.path.dirname(sys.argv[0])
    __find_commit_in = os.path.join(bindir, '__find_commit_in.sh')
    commit_hash = subprocess.check_output([__find_commit_in, author,
        subject, args.upstream_remote]).decode().strip()
    if commit_hash == '':
        print('upstream commit not found')
        exit(1)
    upstream_commit_line = 'commit %s upstream.' % commit_hash

    header_msgs = description.split('\n\n')
    new_description = '\n\n'.join([header_msgs[0], upstream_commit_line] +
        header_msgs[1:])

    user_name = subprocess.check_output(
            'git config --get user.name'.split()).decode().strip()
    user_email = subprocess.check_output(
            'git config --get user.email'.split()).decode().strip()

    new_description += 'Signed-off-by: %s <%s>\n' % (user_name, user_email)
    new_patch = '---\n'.join([new_description] + description_diff[1:])

    with open(args.patch + '.new', 'w') as f:
        f.write(new_patch)

if __name__ == '__main__':
    main()
