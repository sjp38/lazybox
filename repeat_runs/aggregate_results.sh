#!/bin/bash

set -e

# Aggregate multiple results directories into one results directory

if [ $# -lt 3 ]
then
	echo "Usage: $0 <src dir>... <dst dir>"
	exit 1
fi

nr_src_dirs=$(($# - 1))
src_dirs=(${@:1:$nr_src_dirs})
dst_dir="${@: -1}"

bindir=$(dirname "$0")

source "$bindir/__common.sh"

for src_dir in "${src_dirs[@]}"
do
	for v in $VARIANTS
	do
		src="$src_dir/$v"
		dst="$dst_dir/$v"
		mkdir -p "$dst"

		merged=0
		for s in $(find "$src" -name "[0-9][0-9]")
		do
			uid=$(basename "$s")
			candidate="$dst/$uid"
			while [ -d "$candidate" ]
			do
				merged=1
				uid=$((10#$uid + 1))
				uid=$(printf "%02d" $uid)
				candidate="$dst/$uid"
				if [ "$uid" -gt 99 ]
				then
					echo "uid > 99!"
					exit 1
				fi
			done
			echo "cp -R $s $candidate"
			cp -R "$s" "$candidate"
		done

		if [ $merged -ne 0 ]
		then
			continue
		fi

		echo "cp -R $src/* $dst/"
		cp -R "$src/"* "$dst"
	done
done
