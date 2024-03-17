#!/bin/bash

# Show how total number of Linux kernel CVEs that published and rejected by the
# community's CNA changes per day, for last N days.
#
# Example usage:
#     git clone git://git.kernel.org/pub/scm/linux/security/vulns.git
#     ./vulns_stat.sh vulns 30
#    $ ./vulns_stat.sh ~/vulns 30
#    <date> <published> <rejected>
#    2024-02-16      0       0
#    2024-02-17      0       0
#    2024-02-18      0       0
#    2024-02-19      0       0
#    2024-02-20      7       0
#    2024-02-21      14      0
#    2024-02-22      31      1
#    [...]

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
