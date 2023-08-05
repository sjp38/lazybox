#!/usr/bin/env python3

class Change:
    subject = None
    author = None
    description = None
    fixing_changes = None    # list of Change
    diff = None

    def maybe_same(self, other):
        return (type(self) == type(other) and self.subject == other.subject and
                self.author == other.author)

    def fixing(self, other):
        for buggy_change in fixing_changes:
            if buggy_change.maybe_same(other):
                return True
        return False

class Patch:
    change = None
    file_name = None
    sent_date = None
    email_header = None

class Commit:
    change = None
    hashid = None
    author_date = None
