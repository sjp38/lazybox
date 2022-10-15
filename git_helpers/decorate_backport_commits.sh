#!/bin/bash

set -e

if [ $# -ne 3 ]
then
	echo "Usage: $0 <first commit> <last commit> <upstream tree>"
	echo
	echo "Adds upstream commit comments to <first commit>..<last commit>"
	exit 1
fi

bindir=$(dirname "$0")
first_commit=$1
last_commit=$2
remote=$3

commit_range="${first_commit}..${last_commit}"

before_patches_dir=$(mktemp -d before_patches-XXXX)
git format-patch "$commit_range" -o "$before_patches_dir"

after_patches_dir=$(mktemp -d after_patches-XXXX)
for patch in "$before_patches_dir"/*.patch
do
	patch_name=$(basename $patch)
	if ! "$bindir/decorate_backport_patch.py" "$patch" "$remote" > \
		"$after_patches_dir/$patch_name"
	then
		echo "decoration failed, maybe not backported one, no problem"
	fi

done

head_commit=$(git rev-parse HEAD)
commits_to_restore="${last_commit}..${head_commit}"

git reset --hard "$first_commit"

for patch in "$after_patches_dir"/*.patch
do
	git am "$patch"
done

git cherry-pick "$commits_to_restore"

echo "original patches are in $before_patches_dir"
echo "decorated patches are in $after_patches_dir"
