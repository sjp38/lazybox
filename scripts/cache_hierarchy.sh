#!/bin/bash

CACHEDIR=/sys/devices/system/cpu/cpu0/cache/index

for (( idx=0; ; idx++ ))
do
	cachedir=$CACHEDIR$idx
	if [ ! -d "$cachedir" ]
	then
		break
	fi

	level=$(cat "$cachedir/level")

	echo "Level $level"
	echo "======="
	echo ""

	for file in type size ways_of_associativity number_of_sets \
		coherency_line_size;
	do
		printf "$file: %s\n" "$(cat $cachedir/$file)"
	done

	printf "\n\n"
done
