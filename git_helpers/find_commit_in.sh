#!/bin/bash

pr_usage()
{
	echo "Usage: $0 [OPTION]... <commit range>"
	echo
	echo "	Find a commit in <commit range> that has the author name and"
	echo "	subject of <commit>"
	echo
	echo "OPTION"
	echo "  --hash_only	Print hash only"
	echo "  --commit <hash>	Hash of the commit to find"
	echo "  --title <title>	Title of the commit to find"
	exit 1
}

hash_only="false"
while [ $# -ne 0 ]
do
	case $1 in
	"--hash_only")
		hash_only="true"
		shift 1
		continue
		;;
	"--commit")
		if [ $# -lt 2 ]
		then
			pr_usage
		fi
		commit_to_find=$2
		shift 2
		continue
		;;
	"--title")
		if [ $# -lt 2 ]
		then
			pr_usage
		fi
		title_to_find=$2
		shift 2
		continue
		;;
	*)
		if [ $# -ne 1 ]
		then
			pr_usage
		fi
		break
		;;
	esac
done

if [ $# -ne 1 ]
then
	pr_usage
fi
commit_range=$1

if [ "$commit_to_find" = "" ] && [ "$title_to_find" = "" ]
then
	echo "--commit or --title should given"
	pr_usage
fi

if [ "$title_to_find" = "" ]
then
	author=$(git log -n 1 "$commit_to_find" --pretty=%an)
	subject=$(git log -n 1 "$commit_to_find" --pretty=%s)
	hash_subject=$(git log --author="$author" --oneline "$commit_range" | \
		grep -i -m 1 "$subject")

else
	subject="$title_to_find"
	hash_subject=$(git log --oneline "$commit_range" | \
		grep -i -m 1 "$subject")
fi

if [ "$hash_only" = "true" ]
then
	simple_hash=$(echo "$hash_subject" | awk '{print $1}')
	git log --pretty=%H -n 1 "$simple_hash"
	exit
fi

echo "$hash_subject"
