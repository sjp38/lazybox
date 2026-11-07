#!/bin/bash
# SPDX-License-Identifier: GPL-2.0

set -e

if [ $# -ne 2 ]
then
	echo "Usage: $0 <linux_dir> <snapshot_store_dir>"
	exit 1
fi

bindir=$(dirname "$0")
mm_tree_summary_py="$bindir/mm_tree_summary.py"
linux_dir=$1
snapshot_dir=$(realpath $2)
summary_dir=${snapshot_dir}/summary
patches_dir=${snapshot_dir}/patches

if [ -d "${snapshot_dir}/.git" ]
then
	is_git="true"
else
	is_git="false"
fi

exported_commits_info=${summary_dir}/commits_info.json

if [ -f "$exported_commits_info" ]
then
	old_info=$(mktemp old_mm_snapshot_info-XXXXX)
	cp "$exported_commits_info" "$old_info"
else
	old_info=""
fi

if [ "$is_git" = "true" ]
then
	if ! git -C "$snapshot_dir" rm -r "$patches_dir" "$summary_dir"
	then
		echo "initial run?"
	fi
fi

if [ ! -d "$summary_dir" ]
then
	mkdir -p "$summary_dir"
fi

if [ ! -d "$patches_dir" ]
then
	mkdir -p "$patches_dir"
fi

mm_tree_summary_py="$bindir/mm_tree_summary.py"

"$mm_tree_summary_py" --linux_dir "$linux_dir" \
	--export_info "${summary_dir}/commits_info.json" \
	--save_patches "$patches_dir" > /dev/null

"$mm_tree_summary_py" --linux_dir "$linux_dir" \
	--import_info "${summary_dir}/commits_info.json" \
	> "${summary_dir}/summary.md"

"$mm_tree_summary_py" --linux_dir "$linux_dir" \
	--import_info "${summary_dir}/commits_info.json" \
	--full_commits_list \
	> "${summary_dir}/full_commits_list.md"

if [ ! "$old_info" = "" ]
then
	"$mm_tree_summary_py" --linux_dir "$linux_dir" \
		--import_info "${summary_dir}/commits_info.json" \
		--diff_old "$old_info" --list_changed_commits \
		> "${summary_dir}/changes_from_last_update.md"
fi

grep "^MEMORY MANAGEMENT" "${linux_dir}/MAINTAINERS" | while IFS= read -r line
do
	subsystem=$line
	subsys_dir="${summary_dir}/subsystem/$subsystem"
	mkdir -p "$subsys_dir"

	"$mm_tree_summary_py" --linux_dir "$linux_dir" \
		--import_info "${summary_dir}/commits_info.json" \
		--filter allow subsystem "$subsystem" \
		> "${subsys_dir}/summary.md"

	"$mm_tree_summary_py" --linux_dir "$linux_dir" \
		--import_info "${summary_dir}/commits_info.json" \
		--filter allow subsystem "$subsystem" \
		--full_commits_list \
		> "${subsys_dir}/full_commits_list.md"

	if [ ! "$old_info" = "" ]
	then
		"$mm_tree_summary_py" --linux_dir "$linux_dir" \
			--import_info "${summary_dir}/commits_info.json" \
			--filter allow subsystem "$subsystem" \
			--diff_old "$old_info" --list_changed_commits \
			> "${subsys_dir}/changes_from_last_update.md"
	fi
done

if [ ! "$old_info" = "" ]
then
	rm "$old_info"
fi

if [ "$is_git" = "true" ]
then
	git -C "$snapshot_dir" add "$patches_dir" "$summary_dir" > /dev/null
	git -C "$snapshot_dir" commit -as -m "update

This commit was made via $(basename $0).
" > /dev/null
fi

