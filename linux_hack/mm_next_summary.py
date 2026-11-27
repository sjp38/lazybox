#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

'''
Show a summary of mm tree status.
'''

import os

import summary_trees

os.sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'version_control')))

import git_remote_name

def main():
    args = summary_trees.set_get_args(skip_branches_args=True)
    args.git_remote_name = git_remote_name.get_remote_name_for(
            args.linux_dir,
            'git://git.kernel.org/pub/scm/linux/kernel/git/mm/linux.git')
    linus_remote = git_remote_name.get_remote_name_for(
            args.linux_dir,
            'git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git')
    args.baseline = '%s/master' % linus_remote
    args.branch = ['for-next-fixes', 'for-next']
    summary_trees.summary_trees(args)

if __name__ == '__main__':
    main()
