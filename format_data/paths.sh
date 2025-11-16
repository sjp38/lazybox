#!/bin/bash

if [ $# -lt 3 ]
then
	echo "Usage: $0 <prefix> <suffix> <middle [middle...]>"
	exit 1
fi

prefix=$1
suffix=$2
shift
shift
while test $# -gt 0
do
	middles="$middles $1"
	shift
done

for m in $middles
do
	paths="$paths $prefix$m$suffix"
done

echo "$paths"
