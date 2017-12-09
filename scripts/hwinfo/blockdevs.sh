#!/bin/bash

if ! which lsblk > /dev/null
then
	echo "[ERROR] You should install lsblk"
	exit 1
fi

IFS=$'\n'
for l in `lsblk -o MODEL -n | sort`
do
	echo $l
done
