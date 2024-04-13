#!/bin/bash

# Show how total number of Linux kernel CVEs that published and rejected by the
# community's CNA changes per day, for last N days, in M interval.
#
# Example usage:
#    $ git clone git://git.kernel.org/pub/scm/linux/security/vulns.git
#    $ ./vulns_stat.sh ~/vulns/ 46 7
#    <date> <published> <rejected>
#    2024-02-27      103     2
#    2024-03-05      378     4
#    2024-03-12      405     11
#    2024-03-19      456     16
#    2024-03-26      502     18
#    2024-04-02      557     19
#    2024-04-09      692     20

set -e

if [ $# -ne 3 ]
then
	echo "Usage: $0 <vulns repo> <max days to stat> <interval days>"
	exit 1
fi

vulns_path=$1
max_days=$2
interval=$3

if [ ! -d "$vulns_path" ]
then
	echo "$vulns_path no found"
	exit 1
fi

cd "$vulns_path"

git remote update &> /dev/null
git checkout origin/master &> /dev/null

echo "<date> <published> <rejected>"
for ((i = "$max_days" ; i > 0 ; i -= "$interval" ))
do
	date=$(date -d "-$i day" '+%Y-%m-%d')
	commit=$(git log origin/master --until "$date" -1 --pretty=%H)
	nr_cves=$(git ls-tree "$commit" -- cve/published/*/*.json | wc -l)
	nr_rejects=$(git ls-tree "$commit" -- cve/rejected/*/*.json | wc -l)
	echo "$date	$nr_cves	$nr_rejects"
done
