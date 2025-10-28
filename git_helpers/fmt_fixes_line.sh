#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <broken commit>"
	echo "e.g., $0 0123456789ab"
	exit 1
fi

broken=$1
commit_str=$(git log -1 --abbrev=12 --pretty='%h ("%s")' "$broken")
echo "Fixes: ${commit_str}"

# if this is linux kernel repo, further prints Cc: stable@
if ! grep stable@vger.kernel.org MAINTAINERS --quiet &> /dev/null
then
	exit 0
fi
version=$(git describe --contains --match "v*" "$broken")
echo "Cc: <stable@vger.kernel.org> # ${version}"
