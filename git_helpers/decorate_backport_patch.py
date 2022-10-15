#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    '''
    'stable' style adds 'commit xxx upstream.' at the beginning.  Very same to
    the usual stable commits.
    'cherry-pick' style adds '(cherry picked from commit xxx' at the end.  Very
    same to the 'git cherry-pick -x'.
    'both' adds two styles of the comments.
    '''
    parser.add_argument('--upstream_commit_comment_style',
            choices=['stable', 'cherry-pick', 'all'], default='stable',
            help='style of comment for upstream commit')
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

    bindir = os.path.dirname(sys.argv[0])
    find_commit_in = os.path.join(bindir, 'find_commit_in.sh')
    commit_hash = subprocess.check_output([find_commit_in, '--author' author,
        '--title', subject, args.upstream_remote]).decode().strip()
    if commit_hash == '':
        print('upstream commit for %s of %s not found' % (subject, author),
                file=sys.stderr)
        print(patch_content)
        exit(1)

    if args.upstream_commit_comment_style == 'all':
        upstream_commit_comment_styles = ['stable', 'cherry-pick']
    else:
        upstream_commit_comment_styles = [args.upstream_commit_comment_style]

    upstream_commit_line = 'commit %s upstream.' % commit_hash
    cherry_pick_comment = '(cherry picked from commit %s)' % commit_hash

    header_msgs = description.split('\n\n')

    if 'stable' in upstream_commit_comment_styles:
        new_description = '\n\n'.join([header_msgs[0], upstream_commit_line] +
            header_msgs[1:])
    else:
        new_description = '\n\n'.join([header_msgs[0]] + header_msgs[1:])

    user_name = subprocess.check_output(
            'git config --get user.name'.split()).decode().strip()
    user_email = subprocess.check_output(
            'git config --get user.email'.split()).decode().strip()

    new_description += 'Signed-off-by: %s <%s>\n' % (user_name, user_email)
    if 'cherry-pick' in upstream_commit_comment_styles:
        new_description += cherry_pick_comment'\n'
    new_patch = '---\n'.join([new_description] + description_diff[1:])

    print(new_patch)

if __name__ == '__main__':
    main()
