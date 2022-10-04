#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 <commit> <commit range>"
	echo
	echo "	Find a commit in <commit range> that has the author name and"
	echo "	subject of <commit>"
	exit 1
fi

commit_to_find=$1
commit_range=$2

author=$(git log -n 1 "$commit_to_find" --pretty=%an)
subject=$(git log -n 1 "$commit_to_find" --pretty=%s)

git log --author="$author" --oneline "$commit_range" | grep -i -m 1 "$subject"
