#!/bin/bash

find_commit_of_result=""
find_commit_of()
{
	subject=$1
	author=$2
	commit_range=$3

	if [ "$author" = "" ]
	then
		hash_subject=$(git log --oneline "$commit_range" | \
			grep -i -m 1 "$subject")
	else
		hash_subject=$(git log --author "$author" --oneline \
			"$commit_range" | grep -i -m 1 "$subject")
	fi
	find_commit_of_result=$hash_subject
}

pr_usage_exit()
{
	message=$1
	exit_code=$2

	if [ ! "$message" = "" ]
	then
		echo
		echo "$message"
	fi
	echo "
Usage: $0 [OPTION]... <commit range>

Find a commit in <commit range> that has the author name and subject of
<commit>

OPTION
  --hash_only		Print hash only
  --commit <hash>	Hash of the commit to find
  --title <title>	Title of the commit to find
  --author <author>	Author of the commit to find
"
	exit $exit_code
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
			pr_usage_exit "--commit wrong" 1
		fi
		commit_to_find=$2
		shift 2
		continue
		;;
	"--title")
		if [ $# -lt 2 ]
		then
			pr_usage_exit "--title wrong" 1
		fi
		title_to_find=$2
		shift 2
		continue
		;;
	"--author")
		if [ $# -lt 2 ]
		then
			pr_usage_exit "<author> is not given" 1
		fi
		author=$2
		shift 2
		continue
		;;
	*)
		if [ $# -ne 1 ]
		then
			pr_usage_exit "should have <commit range>" 1
		fi
		break
		;;
	esac
done

if [ $# -ne 1 ]
then
	pr_usage_exit "should have <commit range>" 1
fi
commit_range=$1

if [ "$commit_to_find" = "" ] && [ "$title_to_find" = "" ]
then
	pr_usage_exit "--commit or --title should given" 1
fi

if [ "$title_to_find" = "" ]
then
	subject=$(git log -n 1 "$commit_to_find" --pretty=%s)
else
	subject="$title_to_find"
fi

if [ "$author" = "" ] && [ ! "$commit_to_find" = "" ]
then
	author=$(git log -n 1 "$commit_to_find" --pretty=%an)
fi

find_commit_of "$subject" "$author" "$commit_range"
hash_subject=$find_commit_of_result

if [ "$hash_subject" = "" ]
then
	exit 1
fi

if [ "$hash_only" = "true" ]
then
	simple_hash=$(echo "$hash_subject" | awk '{print $1}')
	git log --pretty=%H -n 1 "$simple_hash"
	exit
fi

echo "$hash_subject"
