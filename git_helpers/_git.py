#!/usr/bin/env python3

import os
import sys
import subprocess

class Patch:
    file_name = None
    sent_date = None
    email_header = None
    has_three_dash = None

class Commit:
    hashid = None
    repo = None
    author_date = None

    def git_log(self, pretty_format):
        git_cmd = ['git', '-C', self.repo, 'log', '-1', self.hashid,
                '--pretty=%s' % pretty_format]
        return subprocess.check_output(
                git_cmd, stderr=subprocess.DEVNULL).decode().strip()

    def git_show(self):
        git_cmd = ['git', '-C', self.repo, 'show', self.hashid, '--pretty=']
        return subprocess.check_output(
                git_cmd, stderr=subprocess.DEVNULL).decode().strip()

    def __init__(self, repo, commit_ref):
        self.repo = repo
        git_cmd = ['git', '-C', self.repo, 'log', '-1', commit_ref,
                '--pretty=%H']
        self.hashid = subprocess.check_output(
                git_cmd, stderr=subprocess.DEVNULL).decode().strip()

    def subject(self):
        return self.git_log('%s')

    def author(self):
        return self.git_log('%an <%ae>')

    def author_date(self):
        return self.git_log('%ad')

    def description(self):
        return self.git_log('%b')

    def diff(self):
        return self.git_show()

    def describe(self, contains):
        git_cmd = ['git', '-C', self.repo, 'describe']
        if contains:
            git_cmd.append('--contains')
        return subprocess.check_output(
                git_cmd, stderr=subprocess.DEVNULL).decode().strip()

class Change:
    subject = None
    author = None
    # TODO: Support author date
    description = None
    diff = None
    patch = None
    commit = None

    def set_patch(self, patch_file, set_diff):
        patch = Patch()
        patch.file_name = patch_file

        with open(patch_file, 'rb') as f:
            patch_content = f.read().decode(errors='replace')

        if '\n---\n' in patch_content:
            description_diff = patch_content.split('\n---\n')
            full_description = description_diff[0]
            patch.has_three_dash = True
            if set_diff:
                self.diff = '\n---\n'.join(description_diff[1:])
        else:
            description_diff = patch_content.split('\ndiff --git')
            full_description = description_diff[0]
            patch.has_three_dash = False
            if set_diff:
                self.diff = '\ndiff --git'.join(description_diff[1:])

        # description paragraphs
        desc_pars = full_description.split('\n\n')
        patch.email_header = desc_pars[0]
        self.description = '\n\n'.join(desc_pars[1:]).strip()

        for line in patch.email_header.split('\n'):
            if line.startswith('From: '):
                self.author = line.split('From: ')[1].strip()
            if line.startswith('Date: '):
                patch.sent_date = line.split('Date: ')[1].strip()
            if line.startswith('Subject: [PATCH'):
                subject_fields = line.split(']')[1:]
                self.subject = ']'.join(subject_fields).strip()
            elif line.startswith('Subject: '):
                self.subject = line[len('Subject: '):]

        for line in self.description.split('\n'):
            if line.startswith('From: '):
                self.author = line.split('From: ')[1].strip()
                break

        self.patch = patch

    def set_commit(self, repo, commit_ref, set_diff):
        commit = Commit(repo, commit_ref)

        self.subject = commit.subject()
        self.author = commit.author()
        self.description = commit.description()
        if set_diff:
            self.diff = commit.diff()
        commit.author_date = commit.author_date()
        self.commit = commit

    def __init__(self, subject=None, author=None, patch_file=None,
            commit=None, repo=None, set_diff=False):
        if subject != None:
            self.subject = subject
        if author != None:
            self.author = author
        if patch_file != None:
            self.set_patch(patch_file, set_diff)
        if commit != None:
            self.set_commit(repo, commit, set_diff)

    def maybe_same(self, other):
        if type(self) != type(other):
            return False
        if (self.subject != None and other.subject != None and
                self.subject != other.subject):
            return False
        if (self.author != None and other.author != None and
                self.author != other.author):
            return False
        return True

    def get_fixing_commit_refs(self):
        fixes = []
        for line in self.description.split('\n'):
            if line.startswith('Fixes: '):
                fixes.append(line[len('Fixes: '):])
        return fixes

    def find_matching_commit(self, repo, commits):
        find_commit_in_sh = os.path.join(os.path.dirname(__file__),
                'find_commit_in.sh')
        cmd = [find_commit_in_sh, '--repo', repo, '--hash_only']
        if self.commit and self.commit.hashid:
            cmd += ['--commit', self.commit.hashid]
        else:
            if self.author != None:
                cmd += ['--author', self.author]
            if self.subject != None:
                cmd += ['--title', self.subject]
        cmd += [commits]
        try:
            hashid = subprocess.check_output(cmd).decode().strip()
        except:
            # the change is not in the commits
            return None
        return Change(commit=hashid, repo=repo)

    def find_matching_patch(self, patch_files):
        for patch_file in patch_files:
            change = Change(patch_file=patch_file)
            if self.maybe_same(change):
                return change
        return None

    def find_matching_change(self, files_and_or_commits, repo):
        for file_or_commits in files_and_or_commits:
            if os.path.isfile(file_or_commits):
                patch_file = file_or_commits
                matching_change = self.find_matching_patch([patch_file])
                if matching_change != None:
                    return matching_change
            else:
                commits_range = file_or_commits
                matching_change = self.find_matching_commit(
                        repo, commits_range)
                if matching_change != None:
                    return matching_change
        return None

def read_changes(files_and_or_commits, repo):
    changes = []
    for file_or_commits in files_and_or_commits:
        if os.path.isfile(file_or_commits):
            patch_file = file_or_commits
            changes.append(Change(patch_file=patch_file))
        else:
            commits_range = file_or_commits
            cmd = ['git', '-C', repo, 'log', '--pretty=%H', commits_range]
            commits = subprocess.check_output(cmd).decode().strip().split()
            for commit in commits:
                changes.append(Change(commit=commit, repo=repo))
    return changes
