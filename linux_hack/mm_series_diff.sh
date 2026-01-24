#!/bin/bash

if [ $# -ne 3 ]
then
	echo "Usage: $0 <25-new repo> <before commit> <after commit>"
	exit 1
fi

bindir=$(dirname "$0")
mm_series_diff_py="$bindir/mm_series_diff.py"

mm_series_repo=$(realpath "$1")
before_commit=$2
after_commit=$3

before_tree="${mm_series_repo}/mm_series_diff_worktree.before"
after_tree="${mm_series_repo}/mm_series_diff_worktree.after"

if [ ! -d "$before_tree" ]
then
	git -C "$mm_series_repo" worktree add "$before_tree" "$before_commit"
else
	git -C "$before_tree" checkout "$before_commit"
fi

if [ ! -d "$after_tree" ]
then
	git -C "$mm_series_repo" worktree add "$after_tree" "$after_commit"
else
	git -C "$after_tree" checkout "$after_commit"
fi

"$mm_series_diff_py" "${before_tree}/pc/devel-series" \
	"${after_tree}/pc/devel-series"
