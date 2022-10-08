#!/bin/bash

pr_usage()
{
	echo "Usage: $0 [OPTION]... <commit> <commit range>"
	echo
	echo "	Find a commit in <commit range> that has the author name and"
	echo "	subject of <commit>"
	exit 1
}

if [ $# -lt 2 ]
then
	pr_usage
fi

hash_only="false"
while [ $# -ne 0 ]
do
	case $1 in
	"--hash_only")
		hash_only="true"
		shift 1
		continue
		;;
	*)
		if [ $# -ne 2 ]
		then
			pr_usage
		fi
		break
		;;
	esac
done

commit_to_find=$1
commit_range=$2

author=$(git log -n 1 "$commit_to_find" --pretty=%an)
subject=$(git log -n 1 "$commit_to_find" --pretty=%s)

hash_subject=$(git log --author="$author" --oneline "$commit_range" | \
	grep -i -m 1 "$subject")
if [ "$hash_only" = "true" ]
then
	simple_hash=$(echo "$hash_subject" | awk '{print $1}')
	git log --pretty=%H -n 1 "$simple_hash"
	exit
fi

echo "$hash_subject"
