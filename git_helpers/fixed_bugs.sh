#!/bin/bash

if [ $# -ne 3 ]
then
	echo "Usage: $0 <repo> <bug commits range> <fix commits range>"
	exit 1
fi

repo=$1
potential_bugs=$2
potential_fixes=$3
bindir=$(dirname "$0")

for fix in $(git -C "$repo" log "$potential_fixes" --pretty="%H")
do
	fixes_line=$(git -C "$repo" log -n 1 "$fix" --pretty=%B | \
		grep "^Fixes: ")
	if [ "$fixes_line" = "" ]
	then
		continue
	fi
	bug_commit=$(echo "$fixes_line" | awk '{print $2}')
	if "$bindir/find_commit_in.sh" --repo "$repo" \
		--commit "$bug_commit" "$potential_bugs" &> /dev/null
	then
		echo "$bug_commit in $potential_bugs fixed by $fix in $potential_fixes"
	fi
done
