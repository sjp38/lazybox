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

subject="[hci-noti] $repo_name: $remote/$branch has updated to $commit_intro"

report_file=$(mktemp hci-report-XXXX)

echo "Subject: $subject" > "$report_file"
echo "
humble_ci noticed update on $branch of $url.  The last commit of the tree is:

    $commit_intro" >> "$report_file"

git send-email --to "$recipients" "$report_file"
rm "$report_file"
