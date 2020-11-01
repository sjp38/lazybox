#!/bin/bash

CACHEDIR=/sys/devices/system/cpu/cpu0/cache/index

for (( idx=0; ; idx++ ))
do
	if [ ! -d "$CACHEDIR$idx" ]
	then
		break
	fi

	level=$(cat "$CACHEDIR$idx/level")

	echo "Level $level"
	echo "======="
	echo ""

	for file in type size ways_of_associativity number_of_sets \
		coherency_line_size;
	do
		printf "$file: %s\n" "$(cat $CACHEDIR$idx/$file)"
	done

	printf "\n\n"
done
