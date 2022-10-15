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
    parser.add_argument('upstream_remote', metavar='<remote tree>',
            help='git reference for the upstream tree')
    args = parser.parse_args()

    if args.upstream_commit_comment_style == 'all':
        upstream_commit_comment_styles = ['stable', 'cherry-pick']
    else:
        upstream_commit_comment_styles = [args.upstream_commit_comment_style]

    with open(args.patch, 'r') as f:
        patch_content = f.read()

    # get description and the diff of the patch
    description_diff = patch_content.split('---\n')
    description = description_diff[0]
    diff = '---\n'.join(description_diff[1:])

    # find author and subject of the patch from the description
    author = None
    subject = None
    # description paragraphs
    desc_pars = description.split('\n\n')
    email_header = desc_pars[0]
    for line in email_header.split('\n'):
        if line.startswith('From: '):
            author = line.split('From: ')[1].strip()
        if line.startswith('Subject: [PATCH'):
            subject_fields = line.split(']')[1:]
            subject = ']'.join(subject_fields).strip()
    if author == None or subject == None:
        print('Patch (%s) has no author and subject' % args.patch,
                file=sys.stderr)
        exit(1)

    # find the upstream commit of the patch
    find_commit_in = os.path.join(os.path.dirname(sys.argv[0]),
        'find_commit_in.sh')
    try:
        commit_hash = subprocess.check_output([find_commit_in, '--hash_only',
            '--author', author, '--title', subject,
            args.upstream_remote]).decode().strip()
    except:
        print('upstream commit for %s of %s not found' % (subject, author),
                file=sys.stderr)
        print(patch_content)
        exit(1)

    # format the patch
    cherry_pick_comment = '(cherry picked from commit %s)' % commit_hash

    # new description paragraphs
    new_desc_pars = [email_header]

    if 'stable' in upstream_commit_comment_styles:
        new_desc_pars.append('commit %s upstream.' % commit_hash)
    new_desc_pars += desc_pars[1:]
    new_desc = '\n\n'.join(new_desc_pars)

    user_name = subprocess.check_output(
            'git config --get user.name'.split()).decode().strip()
    user_email = subprocess.check_output(
            'git config --get user.email'.split()).decode().strip()
    signed_off_by_line = 'Signed-off-by: %s <%s>' % (user_name, user_email)

    if new_desc.strip().split('\n')[-1] != signed_off_by_line:
        new_desc += '%s\n' % signed_off_by_line
    if 'cherry-pick' in upstream_commit_comment_styles:
        new_desc += '(cherry picked from commit %s)\n'
    new_patch = '---\n'.join([new_desc, diff])

    print(new_patch)

if __name__ == '__main__':
    main()
