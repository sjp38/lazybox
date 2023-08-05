#!/bin/bash
#
# find patches that fixing some of given commits

bindir=$(dirname "$0")

if [ $# -ne 3 ]
then
	echo "Usage: $0 <commits range> <repo> <patches dir>"
	exit 1
fi

patches_dir=$1
repo_dir=$2
potential_bug_commits=$3

for patch_file in "$patches_dir"/*.patch
do
	bugs=$("$bindir/patch_parse.py" "$patch_file" fixes | awk '{print $1}')
	for bug in $bugs
	do
		bug_in_commits=$("$bindir/find_commit_in.sh" --commit "$bug" \
			--repo "$repo_dir" "$potential_bug_commits")
		if [ ! "$bug_in_commits" = "" ]
		then
			echo "- $patch_file fixes"
			echo "  - $bug_in_commits"
		fi
	done
done
