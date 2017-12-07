#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <pinatrace output file path>"
	exit 1
fi

F=$1

cat $F | awk '{
	if ($1 != "#eof" && $1 != "#" && NF > 3) {
		print NR " " $3
	}
}'
