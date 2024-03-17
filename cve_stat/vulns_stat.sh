#!/bin/bash

# Show how total number of Linux kernel CVEs that published and rejected by the
# community's CNA changes per day, for last N days.

set -e

if [ $# -ne 2 ]
then
	echo "Usage: $0 <vulns repo> <max days to stat>"
	exit 1
fi

vulns_path=$1
max_days=$2

if [ ! -d "$vulns_path" ]
then
	echo "$vulns_path no found"
	exit 1
fi

cd "$vulns_path"

git remote update &> /dev/null
git checkout origin/master &> /dev/null

echo "<date> <published> <rejected>"
for ((i = "$max_days" ; i > 0 ; i-- ))
do
	date=$(date -d "-$i day" '+%Y-%m-%d')
	commit=$(git log origin/master --until "$date" -1 --pretty=%H)
	nr_cves=$(git ls-tree "$commit" -- cve/published/*/*.json | wc -l)
	nr_rejects=$(git ls-tree "$commit" -- cve/rejected/*/*.json | wc -l)
	echo "$date	$nr_cves	$nr_rejects"
done
