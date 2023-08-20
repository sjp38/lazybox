#!/usr/bin/env python3

import subprocess

class CommitInfo:
    hash_id = None
    authored_date = None    # unix timestamp
    committed_date = None   # unix timestamp

    def __init__(self, hash_id, linux_repo):
        # linux_repo: path to the local linux repo
        self.hash_id = hash_id
        self.authored_date, self.committed_date = [int(timestamp)
                for timestamp in subprocess.check_output(
                    ['git', '-C', linux_repo, 'log', '--date=unix',
                        '--pretty=%ad %cd', hash_id, '-1']).decode().split()]

    def days_from_authored_to_committed(self):
        return (self.committed_date - self.authored_date) / (3600 * 24)

# For supporting https://github.com/nluedtke/linux_kernel_cves.git
class LinuxKernelCve:
    name = None             # CVE-ABCD-EFGH
    break_commits = None    # {kernel tree: CommitInfo}
    fix_commits = None      # {kernel tree: CommitInfo}
    cvss_scores = None      # {CVSS version: score}
    added_date = None       # unix timestamp
