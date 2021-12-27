#!/usr/bin/env python3

'''
TODO
- Support author exclusion

DONE
- Support scoping for specific files
- Support linux/MAINTAINERS auto parsing
'''

import argparse
import os
import subprocess

def email_domain(author):
    email = author.split()[-1][1:-1]
    fields = email.split('@')
    return '@'.join(fields[1:])

def parse_git_output_by_commits(git_output, by_domain):
    authors_lines = git_output.split('\n')
    authors = {}
    for author in authors_lines:
        if by_domain:
            author = email_domain(author)
        if not author in authors:
            authors[author] = 0
        authors[author] += 1
    return authors

def parse_git_output_by_lines(git_output, by_domain):
    # example input is:
    #     sj38.park@gmail.com
    #
    #      1 file changed, 1 insertion(+), 1 deletion(-)
    #     sj38.park@gmail.com
    #
    #      1 file changed, 2 insertions(+)

    authors = {}
    lines = git_output.split('\n')
    for idx in range(0, len(lines), 3):
        author = lines[idx].strip()
        if by_domain:
            author = email_domain(author)
        if not author in authors:
            authors[author] = 0
        changes_fields = lines[idx + 2].strip().split()
        for idx, field in enumerate(changes_fields):
            if field in ['insertions(+),', 'insertions(+)', 'deletions(-)',
                    'insertion(+),', 'insertion(+)', 'deletion(-)']:
                authors[author] += int(changes_fields[idx - 1])
    return authors

def parse_git_output(git_output, sortby, by_domain):
    if sortby == 'commits':
        return parse_git_output_by_commits(git_output, by_domain)
    elif sortby == 'lines':
        return parse_git_output_by_lines(git_output, by_domain)
    print('parse_git_output: Wrong sortby (%s)' % sortby)
    exit(1)

def files_for_linux_subsystems(repo, subsystems):
    maintainers_file = os.path.join(repo, 'MAINTAINERS')
    if not os.path.isfile(maintainers_file):
        print('MAINTAINERS file is not found in %s' % repo)
        exit(1)

    with open(maintainers_file, 'r') as f:
        content = f.read()

    maintainers_list = content.split('Maintainers List\n----------------\n')[1]
    subsys_descs = maintainers_list.split('\n\n')[1:]
    if len(subsys_descs) == 0:
        print('subsystems descriptions not found in the MAINTAINERS file')
        exit(1)

    files = []
    for subsys_desc in subsys_descs:
        lines = subsys_desc.strip().split('\n')
        name = lines[0].strip()
        if not name in subsystems:
            continue
        for line in lines[1:]:
            if not line.startswith('F:'):
                continue
            files.append(line.split()[1])
    return files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', metavar='<dir>',
            help='git repositories to get the stat from')
    parser.add_argument('--files', nargs='+', metavar='<file>',
            help='authors for only the files')
    parser.add_argument('--linux_subsystems', nargs='+', metavar='<subsystem>',
            help='authors for the linux subsystems (in MAINTAINERS file)')
    parser.add_argument('--since', metavar='<date>',
            help='since when in YYYY-MM-DD format')
    parser.add_argument('--until', metavar='<date>',
            help='until when in YYYY-MM-DD format')
    parser.add_argument('--max_nr_authors', type=int, metavar='<number>',
            help='max number of authors to list')
    parser.add_argument('--sortby', choices=['commits', 'lines'],
            default='commits', help='metric to sort authors by')
    parser.add_argument('--skip_merge_commits', action='store_true',
            help='do not count merge commits')
    parser.add_argument('--by_domain', action='store_true', default=False,
            help='account by email domain only')
    args = parser.parse_args()

    cmd = ('git -C %s log' % args.repo).split()
    cmd.append('--pretty=%an <%ae>')
    if args.since:
        cmd.append('--since=%s' % args.since)
    if args.until:
        cmd.append('--until=%s' % args.until)
    if args.sortby == 'lines':
        cmd.append('--shortstat')
        args.skip_merge_commits = True
    if args.skip_merge_commits:
        cmd.append('--no-merges')

    if args.linux_subsystems:
        if args.files == None:
            args.files = []
        args.files += files_for_linux_subsystems(args.repo,
                args.linux_subsystems)

    if args.files:
        cmd.append('--')
        cmd += args.files

    git_output = subprocess.check_output(cmd).decode().strip()
    authors = parse_git_output(git_output, args.sortby, args.by_domain)

    authors_sorted = sorted(authors, key=authors.get, reverse=True)
    if args.max_nr_authors:
        authors_sorted = authors_sorted[:args.max_nr_authors]
    for author in authors_sorted:
        print('%s: %d %s' % (author, authors[author], args.sortby))

    print('# %d authors, %d %s in total' % (len(authors),
        sum(authors.values()), args.sortby))

if __name__ == '__main__':
    main()
