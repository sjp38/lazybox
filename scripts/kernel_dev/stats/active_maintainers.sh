#!/bin/bash

if [ $# -lt 1 ]
then
	echo "Usage: $0 <linux repo> [activeness threshold in days]"
	exit 1
fi

linux_repo=$1

if [ $# -ge 2 ]
then
	active_thres_days=$2
else
	active_thres_days=180
fi

maintainers=$(git -C "$linux_repo" show HEAD:MAINTAINERS 2> /dev/null | \
	grep '^M:' | sort | uniq | awk -F'^M:\t' '{print $2}')
nr_maintainers=$(echo "$maintainers" | wc -l)

since_date=$(date --date="-$active_thres_days day")
nr_active_maintainers=0
while IFS= read -r author
do
	email=$(echo "$author" | awk '{print $NF}')
	nr_recent_commits=$(git -C "$linux_repo" \
		log --pretty=%h --since "$since_date" \
		--author "$email" -1 | wc -l)
	if [ "$nr_recent_commits" -eq 1 ]
	then
		echo "$author": active
		nr_active_maintainers=$((nr_active_maintainers + 1))
	else
		echo "$author": inactive
	fi
done <<< "$maintainers"

echo "$nr_maintainers	$nr_active_maintainers"
