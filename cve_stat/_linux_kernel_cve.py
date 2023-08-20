#!/usr/bin/env python3

class CommitInfo:
    hash_id = None
    authored_date = None    # unix timestamp
    committed_date = None   # unix timestamp

# For supporting https://github.com/nluedtke/linux_kernel_cves.git
class LinuxKernelCve:
    name = None             # CVE-ABCD-EFGH
    break_commits = None    # {kernel tree: CommitInfo}
    fix_commits = None      # {kernel tree: CommitInfo}
    cvss_scores = None      # {CVSS version: score}
    added_date = None       # unix timestamp
