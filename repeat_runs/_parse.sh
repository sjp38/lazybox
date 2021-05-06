#!/bin/bash

BINDIR=$(dirname "$0")

source "$BINDIR/__common.sh"

if [ $# -ne 2 ]
then
	echo "Usage: $0 <experiment dir> <raw output directory>"
	exit 1
fi

if [ -z "$parsers_dir" ]
then
	parsers_dir="$1/parsers/"
fi
raw_outputs_dir=$2
parsed_dir="$raw_outputs_dir/$PARSED"

mkdir -p "$parsed_dir"

echo "parse $raw_outputs_dir"
for raw_output in $(ls "$raw_outputs_dir")
do
	parsers=$(ls "$parsers_dir" | grep -e '^'"$raw_output"'*')
	for parser in $parsers
	do
		"$parsers_dir"/"$parser" "$raw_outputs_dir" "$parsed_dir"
	done
done
