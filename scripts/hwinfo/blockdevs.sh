#!/bin/bash

if ! which lsblk > /dev/null
then
	echo "[ERROR] You should install lsblk"
	exit 1
fi

IFS=$'\n'
for l in `lsblk -o MODEL,SIZE -n | sort`
do
	echo $l | awk '{
		if (NF < 2) {
			next
		}
		for (i = 1; i < NF; i++) {
			printf $i " "
		}
		printf "(" $i ")\n"
	}'
done
