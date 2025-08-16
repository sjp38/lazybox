#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <broken commit>"
	echo "e.g., $0 0123456789ab"
	exit 1
fi

broken=$1
commit_str=$(git log -1 --abbrev=12 --pretty='%h ("%s")' "$broken")
version=$(git describe --contains --match "v*" "$broken")
echo "Fixes: ${commit_str} # ${version}"
