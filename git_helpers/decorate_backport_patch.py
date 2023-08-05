#!/usr/bin/env python3

import argparse
import sys

import _patch

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

    patch = _patch.Patch(args.patch)
    if patch.author == None or patch.subject == None:
        print('Patch (%s) has no author and subject' % args.patch,
                file=sys.stderr)
        exit(1)

    try:
        commit_hash = patch.commit_in(args.upstream_remote)
    except:
        print('upstream commit for %s of %s not found' %
                (patch.subject, patch.author), file=sys.stderr)
        sys.stdout.write('%s' % patch)
        exit(1)

    patch.decorate_for_backport(commit_hash, upstream_commit_comment_styles)
    sys.stdout.write('%s' % patch)

if __name__ == '__main__':
    main()
