#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <linux repo>"
	exit 1
fi

linux_repo=$1

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
		echo "$version: $nr_maintainers"
	done
done
