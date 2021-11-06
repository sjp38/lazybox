#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <linux repo>"
	exit 1
fi

linux_repo=$1

echo "version	total	new"

prev_nr_maintainers=0
for major in 2.6 3 4 5
do
	for minor in {1..40}
	do
		version="v$major.$minor"
		nr_maintainers=$(git -C "$linux_repo" \
			show "$version":MAINTAINERS 2> /dev/null | \
			grep '^M:' | sort | uniq -c | wc -l)
		if [ "$nr_maintainers" = "0" ]
		then
			continue
		fi

		if [ "$prev_nr_maintainers" -eq 0 ]
		then
			new=0
		else
			new=$((nr_maintainers - prev_nr_maintainers))
		fi

		echo "$version	$nr_maintainers	$new"
		prev_nr_maintainers=$nr_maintainers
	done
done
