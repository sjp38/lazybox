#!/usr/bin/env python3

'''
TODO
- Exclude/include specific email domain
- Support plotting

DONE
- Support author exclusion
- Support scoping for specific files
- Support linux/MAINTAINERS auto parsing
- Identify authors using only name
- Make --max_nr_authors 30 by default
- Print rank of each authors in output
- Support outputs per interval (e.g., --since 2020-01-01 --until 2022-12-31 --interval 30days)
'''

import argparse
import collections
import datetime
import os
import subprocess

def author_id(author, identify_with):
    if identify_with == 'all':
        return author
    elif identify_with == 'name':
        return ' '.join(author.split()[0:-1])
    elif identify_with == 'email':
        return author.split()[-1][1:-1]
    elif identify_with == 'domain':
        email = author.split()[-1][1:-1]
        fields = email.split('@')
        return '@'.join(fields[1:])

def parse_git_output_by_commits(git_output, author_identity):
    authors_lines = git_output.split('\n')
    authors = {}
    for author in authors_lines:
        if author == '':
            continue
        author = author_id(author, author_identity)
        if not author in authors:
            authors[author] = 0
        authors[author] += 1
    return authors

def parse_git_output_by_lines(git_output, author_identity):
    # example input is:
    #     sj38.park@gmail.com <- empty commit
    #     sj38.park@gmail.com
    #
    #      1 file changed, 1 insertion(+), 1 deletion(-)
    #     sj38.park@gmail.com
    #
    #      1 file changed, 2 insertions(+)

    authors = {}
    lines = git_output.split('\n')
    idx =0
    while idx < len(lines):
        author = lines[idx].strip()
        author = author_id(author, author_identity)
        if 'changed' in author:
            print('changed in line %d (%s)' % (idx, author))
            print('\n'.join(lines))
            exit(0)
        if not author in authors:
            authors[author] = 0
        if idx == len(lines) - 1 or lines[idx + 1] != '':
            # empty commit
            idx += 1
            continue
        changes_fields = lines[idx + 2].strip().split()
        for idx2, field in enumerate(changes_fields):
            if field in ['insertions(+),', 'insertions(+)', 'deletions(-)',
                    'insertion(+),', 'insertion(+)', 'deletion(-)']:
                authors[author] += int(changes_fields[idx2 - 1])
        idx += 3
    return authors

def parse_git_output(git_output, sortby, author_identity):
    if sortby == 'commits':
        return parse_git_output_by_commits(git_output, author_identity)
    elif sortby == 'lines':
        return parse_git_output_by_lines(git_output, author_identity)
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

def get_authors(args):
    cmd = ('git -C %s log' % args.repo).split()
    cmd.append('--pretty=%an <%ae>')
    if args.commits_range:
        cmd.append('%s' % args.commits_range)
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
    authors = parse_git_output(git_output, args.sortby, args.author_identity)
    if args.exclude:
        authors = {k:v for k,v in authors.items() if not k in args.exclude}
    authors_sorted = sorted(authors, key=authors.get, reverse=True)
    if args.max_nr_authors:
        authors_sorted = authors_sorted[:args.max_nr_authors]
    return authors_sorted, authors

def pr_authors(authors_sorted, authors, sortby, hide_rank, pr_for_plot):
    if pr_for_plot:
        print(sortby)
    for idx, author in enumerate(authors_sorted):
        if pr_for_plot:
            line = '%d %d' % (idx, authors[author])
        else:
            line = '%s: %d %s' % (author, authors[author], sortby)
            if not hide_rank:
                line = '%d. %s' % (idx + 1, line)
        print(line)

    print('# %d authors, %d %s in total' % (len(authors),
        sum(authors.values()), sortby))

def get_pr_authors(args):
    pr_authors(*get_authors(args), args.sortby, args.hide_rank,
            args.pr_for_plot)

def yyyymmdd_to_date(yyyymmdd):
    return datetime.date(*[int(x) for x in yyyymmdd.split('-')])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', metavar='<dir>',
            help='git repositories to get the stat from')
    parser.add_argument('--commits_range', metavar='<commits range>',
            help='git commits range to get the stat from')
    parser.add_argument('--files', nargs='+', metavar='<file>',
            help='authors for only the files')
    parser.add_argument('--linux_subsystems', nargs='+', metavar='<subsystem>',
            help='authors for the linux subsystems (in MAINTAINERS file)')
    parser.add_argument('--since', metavar='<date>',
            help='since when in YYYY-MM-DD format')
    parser.add_argument('--until', metavar='<date>',
            help='until when in YYYY-MM-DD format')
    parser.add_argument('--interval', metavar='<days>', type=int,
            help='interval days to print output for each')
    parser.add_argument('--exclude', metavar='<author>', nargs='+',
            help='authors to exclude from the output')
    parser.add_argument('--max_nr_authors', type=int, metavar='<number>',
            default=30,
            help='max number of authors to list')
    parser.add_argument('--sortby', choices=['commits', 'lines'],
            default='commits', help='metric to sort authors by')
    parser.add_argument('--skip_merge_commits', action='store_true',
            help='do not count merge commits')
    parser.add_argument('--author_identity', default='all',
            choices=['all', 'name', 'email', 'domain'],
            help='how to identify authors')
    parser.add_argument('--hide_rank', action='store_true',
            help='do not print rank')
    parser.add_argument('--pr_by_authors', action='store_true',
            help='print output by authors')
    parser.add_argument('--pr_for_plot', action='store_true',
            help='print output for easy plotting')
    args = parser.parse_args()

    if args.interval:
        if not args.since:
            print('\'--interval\' should given with \'--since\'')
            exit(1)
        orig_until = args.until
        if not orig_until:
            orig_until = datetime.date.today().strftime('%Y-%m-%d')
        args.until = yyyymmdd_to_date(args.since) + datetime.timedelta(
                args.interval)
        args.until = args.until.strftime('%Y-%m-%d')

        if args.pr_by_authors:
            authors_by_time = []
            while yyyymmdd_to_date(args.since) < yyyymmdd_to_date(orig_until):
                period = '%s to %s' % (args.since, args.until)
                authors_by_time.append([period, get_authors(args)])
                args.since = args.until
                args.until = yyyymmdd_to_date(args.since) + datetime.timedelta(
                        args.interval)
                args.until = args.until.strftime('%Y-%m-%d')
            total_authors = []
            for period, authors in authors_by_time:
                authors_sorted = authors[0]
                for author in authors_sorted:
                    if not author in total_authors:
                        total_authors.append(author)
            for author in total_authors:
                print('author:', author)
                for period, authors in authors_by_time:
                    authors_contribs = authors[1]
                    contribs = 0
                    if author in authors_contribs:
                        contribs = authors_contribs[author]
                    print(period, contribs, args.sortby)
                print()
            return

        while yyyymmdd_to_date(args.since) < yyyymmdd_to_date(orig_until):
            print('\n# %s to %s' % (args.since, args.until))
            get_pr_authors(args)
            args.since = args.until
            args.until = yyyymmdd_to_date(args.since) + datetime.timedelta(
                    args.interval)
            args.until = args.until.strftime('%Y-%m-%d')
        return

    get_pr_authors(args)

if __name__ == '__main__':
    main()
