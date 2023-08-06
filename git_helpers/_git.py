#!/usr/bin/env python3

import os
import subprocess

class Change:
    subject = None
    author = None
    description = None
    fixing_changes = None    # list of Change
    diff = None
    patch = None
    commit = None

    def maybe_same(self, other):
        return (type(self) == type(other) and self.subject == other.subject and
                self.author == other.author)

    def fixing(self, other, repo):
        for buggy_change in self.fixing_changes:
            if buggy_change.author == None and repo != None:
                buggy_change.commit.set_repo_and_missing_fields(repo)
            if buggy_change.maybe_same(other):
                return True
        return False

    def commit_in(self, repo, commits):
        find_commit_in_sh = os.path.join(os.path.dirname(sys.argv[0]),
                'find_commit_in.sh')
        cmd = [find_commit_in_sh, '--repo', repo, '--hash_only']
        if self.commit and self.commit.hashid:
            cmd += ['--commit', self.commit.hashid]
        else:
            cmd += ['--author', self.author, '--title', self.subject]
        cmd += [commits]
        try:
            hashid = subprocess.check_output(cmd).decode().strip()
        except:
            # the change is not in the commits
            return None
        return Commit(hashid, repo)

    def patch_in(self, patch_files):
        for patch_file in patch_files:
            patch = Patch(patch_file)
            if self.maybe_same(patch):
                return patch
        return None

class Patch:
    change = None
    file_name = None
    sent_date = None
    email_header = None
    has_three_dash = None

    def __init__(self, filepath, set_diff=False):
        self.file_name = filepath

        change = Change()
        with open(filepath, 'rb') as f:
            patch_content = f.read().decode(errors='replace')

        if '\n---\n' in patch_content:
            description_diff = patch_content.split('\n---\n')
            full_description = description_diff[0]
            self.has_three_dash = True
            if set_diff:
                change.diff = '\n---\n'.join(description_diff[1:])
        else:
            description_diff = patch_content.split('\ndiff --git')
            full_description = description_diff[0]
            self.has_three_dash = False
            if set_diff:
                change.diff = '\ndiff --git'.join(description_diff[1:])

        # description paragraphs
        desc_pars = full_description.split('\n\n')
        self.email_header = desc_pars[0]
        change.description = '\n\n'.join(desc_pars[1:]).strip()

        for line in self.email_header.split('\n'):
            if line.startswith('From: '):
                change.author = line.split('From: ')[1].strip()
            if line.startswith('Date: '):
                self.sent_date = line.split('Date: ')[1].strip()
            if line.startswith('Subject: [PATCH'):
                subject_fields = line.split(']')[1:]
                change.subject = ']'.join(subject_fields).strip()
            elif line.startswith('Subject: '):
                change.subject = line[len('Subject: '):]

        change.fixing_changes = []
        for line in change.description.split('\n'):
            if line.startswith ('From: '):
                change.author = line.split('From: ')[1].strip()
            if line.startswith('Fixes: '):
                # usual format is: Fixes: <hash 12 letter> ("<subject>")
                fixes_content = line[len('Fixes: '):].strip()
                commit_hash = fixes_content.split()[0]
                fixing_changes.append(Commit(commit_hash, None).change)

        self.change = change
        change.patch = self

class Commit:
    hashid = None
    repo = None
    change = None
    author_date = None

    def git_log(self, pretty_format):
        git_cmd = ['git', '-C', self.repo, 'log', '-1', self.hashid,
                '--pretty=%s' % pretty_format]
        return subprocess.check_output(git_cmd).decode().strip()

    def git_show(self):
        git_cmd = ['git', '-C', self.repo, 'show', self.hashid, '--pretty=']
        return subprocess.check_output(git_cmd).decode().strip()

    def set_repo_and_missing_fields(self, repo, set_diff=False):
        self.repo = repo
        change = self.change
        change.subject = self.git_log('%s')
        author_name = self.git_log('%an')
        author_email = self.git_log('%ae')
        change.author = '%s <%s>' % (author_name, author_email)
        change.description = self.git_log('%b')
        if set_diff:
            change.diff = self.git_show()
        self.author_date = self.git_log('%ad')

    def __init__(self, hashid, repo, set_diff=False):
        self.hashid = hashid
        self.change = Change()
        self.change.commit = self
        if repo == None:
            return
        self.repo = os.path.abspath(repo)
        self.set_repo_and_missing_fields(repo, set_diff)
