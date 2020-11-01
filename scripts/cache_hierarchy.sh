#!/bin/bash

CACHEDIR=/sys/devices/system/cpu/cpu0/cache/index

for (( level=0; ; level++ ))
do
	if [ ! -d "$CACHEDIR$level" ]
	then
		break
	fi

	echo "Level $level"
	echo "======="
	echo ""

	for file in type size ways_of_associativity number_of_sets \
		coherency_line_size;
	do
		printf "$file: %s\n" "$(cat $CACHEDIR$level/$file)"
	done

	printf "\n\n"
done
