#!/usr/bin/env python3

import argparse
import subprocess

remote_name = 'akpm.korg.mm'

mm_master = 'akpm.korg.mm/master'
mm_stable = 'akpm.korg.mm/mm-stable'
mm_unstable = 'akpm.korg.mm/mm-unstable'
mm_new = 'akpm.korg.mm/mm-new'

def pr_branch(commit, branches_to_show, nr_branch_commits):
    for branch_name, branch_commit in branches_to_show:
        if commit == branch_commit:
            print('%s (%d patches)' % (branch_name, nr_branch_commits))
            print()
            nr_branch_commits = 0
    return nr_branch_commits


def list_patches_in(commits_base, commits_end, min_len_single_patch,
                    branches_to_show):
    cproc = subprocess.run(
            ['git', 'log', '--pretty=%H', '--reverse', '%s..%s' %
             (commits_base, commits_end)],
            capture_output=True, text=True)
    if cproc.returncode != 0:
        return 'git log fail (%s)' % cproc.stderr
    commits = [x for x in cproc.stdout.strip().split('\n') if x != '']
    print('%d patches in total' % len(commits))
    print()
    to_skip = 0
    nr_branch_commits = 0
    for commit in commits:
        nr_branch_commits += 1
        if to_skip > 0:
            to_skip -= 1
            nr_branch_commits = pr_branch(commit, branches_to_show,
                                          nr_branch_commits)
            continue
        cproc = subprocess.run(
                ['git', 'log', '-1', '--pretty=%B', commit],
                capture_output=True, text=True)
        if cproc.returncode != 0:
            return 'git log -1 fail (%s)' % cproc.stderr
        commit_msg = cproc.stdout.strip()
        pars = commit_msg.split('\n\n')
        if len(pars) < 2:
            continue
        patch_series_par = pars[1]
        if patch_series_par.strip().startswith('Patch series '):
            unwrapped = ' '.join(patch_series_par.split('\n'))
            print('    %s' % unwrapped)
            # skip next commits of the series
            for line in commit_msg.split('\n'):
                if line.startswith('This patch (of ') and line.endswith('):'):
                    to_skip = int(line.split()[3][:-2]) - 1
            continue
        cproc = subprocess.run(
                ['git', 'show', commit, '--pretty=%h'], capture_output=True,
                text=True)
        if cproc.returncode != 0:
            return 'git show fail (%s)' % cproc.stderr
        commit_content = cproc.stdout
        if len(commit_content.split('\n')) > min_len_single_patch:
            unwrapped = ' '.join(pars[0].split('\n'))
            print('    Patch "%s"' % unwrapped)
        nr_branch_commits = pr_branch(commit, branches_to_show,
                                      nr_branch_commits)
    print()
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--min_len_single_patch', type=int, default=0)
    args = parser.parse_args()

    mm_master_desc = subprocess.check_output(
            ['git', 'describe', mm_master]).decode()
    print('mm/master: %s' % mm_master_desc)

    branch_name_commit_list = []
    for branch_name in ['mm-stable', 'mm-unstable', 'mm-new',
                        'mm-hotfixes-stable', 'mm-hotfixes-unstable']:
        commit_id = subprocess.check_output(
                ['git', 'rev-parse', '%s/%s' % (
                    remote_name, branch_name)]).decode().strip()
        branch_name_commit_list.append([branch_name, commit_id])

    err = list_patches_in(mm_master, mm_new, args.min_len_single_patch,
                          branch_name_commit_list)
    if err is not None:
        print(err)
        exit(1)

if __name__ == '__main__':
    main()
