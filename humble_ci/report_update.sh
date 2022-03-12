#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <receipients>"
	exit 1
fi

recipients=$1

repo=$HUMBLE_CI_REPO
remote=$HUMBLE_CI_REMOTE
url=$HUMBLE_CI_URL
branch=$HUMBLE_CI_BRANCH

repo_name=$(basename "$repo")

commit_intro=$(git -C "$repo" show --pretty="%h (\"%s\")" --quiet \
	"$remote/$branch")

subject="$repo_name: $remote/$branch has updated to $commit_intro"
echo "Subject: $subject" > report
echo "
humble_ci noticed $repo_name's update on $branch of $remote ($url).
The latest commit of the tree is:

    $commit_intro" >> report

git send-email --to "$recipients" report
rm report
