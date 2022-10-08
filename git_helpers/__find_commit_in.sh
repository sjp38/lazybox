#!/bin/bash

if [ $# -ne 3 ]
then
	echo "Usage: $0 <author> <subject> <commit range>"
	echo
	echo "	Find a commit in <commit range> that has the <author> and the"
	echo "	<subject>"
	exit 1
fi

author=$1
subject=$2
commit_range=$3

hash=$(git log --author="$author" --oneline "$commit_range" | \
	grep -i -m 1 "$subject" | awk '{print $1}')
git log -n 1 --pretty=%H $hash
