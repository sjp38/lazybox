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
            'https://git.kernel.org/pub/scm/linux/kernel/git/akpm/mm.git')
    args.baseline = '%s/master' % args.git_remote_name
    args.branch = ['mm-hotfixes-stable', 'mm-hotfixes-unstable',
                     'mm-stable', 'mm-unstable', 'mm-new',
                     'mm-nonmm-stable', 'mm-nonmm-unstable']
    summary_trees.summary_trees(args)

if __name__ == '__main__':
    main()
