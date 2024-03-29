#!/usr/bin/env python3

import json
import os
import subprocess

class CommitInfo:
    hash_id = None
    authored_date = None    # unix timestamp
    committed_date = None   # unix timestamp

    def __init__(self, hash_id, linux_repo):
        # linux_repo: path to the local linux repo
        self.hash_id = hash_id
        if not self.hash_id:
            return
        try:
            self.authored_date, self.committed_date = [int(timestamp)
                    for timestamp in subprocess.check_output([
                        'git', '-C', linux_repo, 'log', '--date=unix',
                        '--pretty=%ad %cd', hash_id, '-1']).decode().split()]
        except Exception as e:
            print('failed getting commit info for %s (%s)' % (hash_id, e))

    def days_from_authored_to_committed(self):
        return (self.committed_date - self.authored_date) / (3600 * 24)

    def to_kvpairs(self):
        return self.__dict__

    @classmethod
    def from_kvpairs(cls, kvpairs):
        obj = cls.__new__(cls)
        obj.hash_id = kvpairs['hash_id']
        obj.authored_date = kvpairs['authored_date']
        obj.committed_date = kvpairs['committed_date']
        return obj

# For supporting https://github.com/nluedtke/linux_kernel_cves.git
class LinuxKernelCve:
    name = None             # CVE-ABCD-EFGH
    break_commits = None    # {kernel tree: CommitInfo}
    fix_commits = None      # {kernel tree: CommitInfo}
    cvss_scores = None      # {CVSS version: score}
    added_date = None       # unix timestamp
    add_commit_id = None

    def __init__(self, name, linux_kernel_cves_repo,
            main_infos, stream_breaks, stream_fixes, linux_repo):
        # linux_kernel_cves_repo: path to linux_kernel_cves local repo
        # main_infos: linux_kernel_cves/data/kernel_cves.json parsed dict
        # stream_breaks: linux_kernel_cves/data/stream_data.json parsed dict
        # stream_fixes: linux_kernel_cves/data/stream_fixes.json parsed dict
        # linux_repo: path to linux local repo

        data_dir=os.path.join(linux_kernel_cves_repo, 'data')
        if main_infos == None:
            with open(os.path.join(data_dir, 'kernel_cves.json'), 'r') as f:
                main_infos = json.load(f)
        if stream_breaks == None:
            with open(os.path.join(data_dir, 'stream_data.json'), 'r') as f:
                stream_breaks = json.load(f)
        if stream_fixes == None:
            with open(os.path.join(data_dir, 'stream_fixes.json'), 'r') as f:
                stream_fixes = json.load(f)

        self.name = name

        if not name in main_infos:
            return
        main_info = main_infos[name]

        self.break_commits = {}
        if 'breaks' in main_info:
            self.break_commits['mainline'] = CommitInfo(
                    main_info['breaks'], linux_repo)
            for stable_series, series_breaks in stream_breaks.items():
                for stable_release, breaks in series_breaks.items():
                    if not name in breaks:
                        continue
                    break_info = breaks[name]
                    if not 'cmt_id' in break_info:
                        continue
                    self.break_commits[stable_series] = CommitInfo(
                            break_info['cmt_id'], linux_repo)

        self.fix_commits = {}
        if 'fixes' in main_info:
            self.fix_commits['mainline'] = CommitInfo(
                    main_info['fixes'], linux_repo)
            if name in stream_fixes:
                for series, fixes in stream_fixes[name].items():
                    self.fix_commits[series] = CommitInfo(
                            fixes['cmt_id'], linux_repo)

        self.cvss_scores = {}
        if 'cvss1' in main_info and 'score' in main_info['cvss1']:
            self.cvss_scores['cvss1'] = main_info['cvss1']['score']
        if 'cvss2' in main_info and 'score' in main_info['cvss2']:
            self.cvss_scores['cvss2'] = main_info['cvss2']['score']
        if 'cvss3' in main_info and 'score' in main_info['cvss3']:
            self.cvss_scores['cvss3'] = main_info['cvss3']['score']

        data_file = os.path.join(data_dir, 'kernel_cves.json')
        cve_line_number = int(subprocess.check_output([
            'grep', '-n', '--max-count=1', '    "%s":' % name,
            data_file]).decode().split(':')[0])
        self.add_commit_id = subprocess.check_output([
            'git', '-C', linux_kernel_cves_repo, 'blame',
            os.path.join('data', 'kernel_cves.json'),
            '-L', '%d,%d' % (cve_line_number,
                cve_line_number)]).decode().split()[0]
        self.added_date = int(subprocess.check_output([
            'git', '-C', linux_kernel_cves_repo, 'log', '-1', '--date=unix',
            '--pretty=%ad', self.add_commit_id]).decode().strip())

    def to_kvpairs(self):
        kvpairs = self.__dict__
        for tree, commitinfo in self.fix_commits.items():
            kvpairs['fix_commits'][tree] = commitinfo.to_kvpairs()
        for tree, commitinfo in self.break_commits.items():
            kvpairs['break_commits'][tree] = commitinfo.to_kvpairs()
        return kvpairs

    @classmethod
    def from_kvpairs(cls, kvpairs):
        obj = cls.__new__(cls)
        obj.name = kvpairs['name']
        obj.break_commits = {}
        for tree, commit_info in kvpairs['break_commits'].items():
            try:
                obj.break_commits[tree] = CommitInfo.from_kvpairs(commit_info)
            except:
                pass
        obj.fix_commits = {}
        for tree, commit_info in kvpairs['fix_commits'].items():
            try:
                obj.fix_commits[tree] = CommitInfo.from_kvpairs(commit_info)
            except:
                pass
        obj.cvss_scores = kvpairs['cvss_scores']
        obj.added_date = kvpairs['added_date']
        obj.add_commit_id = kvpairs['add_commit_id']
        return obj

def load_kernel_cves_from_json(json_file):
    with open(json_file, 'r') as f:
        kvpairs = json.load(f)
    return {name: LinuxKernelCve.from_kvpairs(cve_kvpairs)
            for name, cve_kvpairs in kvpairs.items()}
