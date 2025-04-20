#!/usr/bin/env python3

import subprocess

mm_master = 'akpm.korg.mm/master'
mm_stable = 'akpm.korg.mm/mm-stable'
mm_unstable = 'akpm.korg.mm/mm-unstable'
mm_new = 'akpm.korg.mm/mm-new'

def list_patches_in(commits_base, commits_end):
    cproc = subprocess.run(
            ['git', 'log', '--pretty=%H', '--reverse', '%s..%s' %
             (commits_base, commits_end)],
            capture_output=True, text=True)
    if cproc.returncode != 0:
        return 'git log fail (%s)' % cproc.stderr
    commits = [x for x in cproc.stdout.strip().split('\n') if x != '']
    print('%s: %d patches' % (commits_end.split('/')[-1], len(commits)))
    to_skip = 0
    for commit in commits:
        if to_skip > 0:
            to_skip -= 1
            continue
        cproc = subprocess.run(
                ['git', 'log', '-1', '--pretty=%B', commit],
                capture_output=True, text=True)
        if cproc.returncode != 0:
            return 'git log -1 fail (%s)' % cproc.stderr
        commit_msg = cproc.stdout.strip()
        pars = commit_msg.split('\n\n')
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
        if len(commit_content.split('\n')) > 300:
            unwrapped = ' '.join(pars[0].split('\n'))
            print('    Patch "%s"' % unwrapped)
    print()
    return None

def main():
    err = list_patches_in(mm_master, mm_stable)
    if err is not None:
        print(err)
        exit(1)
    err = list_patches_in(mm_stable, mm_unstable)
    if err is not None:
        print(err)
        exit(1)
    err = list_patches_in(mm_unstable, mm_new)
    if err is not None:
        print(err)
        exit(1)

if __name__ == '__main__':
    main()
