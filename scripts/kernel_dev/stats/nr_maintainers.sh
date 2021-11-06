#!/bin/bash

for major in 2.6 3 4 5
do
	for minor in {1..20}
	do
		version="v$major.$minor"
		nr_maintainers=$(git show "$version":MAINTAINERS 2> /dev/null | \
			grep '^M:' | sort | uniq -c | wc -l)
		if [ "$nr_maintainers" = "0" ]
		then
			continue
		fi
		echo "$version: $nr_maintainers"
	done
done
