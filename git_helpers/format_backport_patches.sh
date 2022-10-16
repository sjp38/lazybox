#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 <commits range> <upstream tree>"
	exit 1
fi

bindir=$(dirname "$0")
commit_range=$1
remote=$2

before_patches_dir=$(mktemp -d before_patches-XXXX)
echo "convert $commit_range into patches under \"$before_patches_dir/\""
git format-patch "$commit_range" -o "$before_patches_dir" --quiet

after_patches_dir=$(mktemp -d after_patches-XXXX)
for patch in "$before_patches_dir"/*.patch
do
	echo "decorate $patch"
	patch_name=$(basename $patch)
	if ! "$bindir/decorate_backport_patch.py" "$patch" "$remote" > \
		"$after_patches_dir/$patch_name" 2> /dev/null
	then
		echo "	decoration failed, maybe not a backported one"
	fi
done

echo "Not decorated patches are in ${before_patches_dir}/"
echo "Decorated patches are in ${after_patches_dir}/"
