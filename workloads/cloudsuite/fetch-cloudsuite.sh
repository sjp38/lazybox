#!/bin/bash

# Because official cloudsuite is updated often, we use a fork.
REPO="https://github.com/sjp38/cloudsuite-personal.git"
TARGET_DIR="cloudsuite"
TARGET_REV="e48bc2434bc2d15fcec7f496245726a6a35ca000"

if ! which git
then
	echo "[Error] git not found. Please install it."
	exit 1
fi

if [ -d $TARGET_DIR ]
then
	cd $TARGET_DIR
	if [ $TARGET_REV == $(git rev-parse HEAD) ]
	then
		echo "Already fetched.  Nothing to do."
		exit 0
	else
		echo "$TARGET_DIR directory should be removed first."
		exit 1
	fi
fi

git clone $REPO $TARGET_DIR
cd $TARGET_DIR
git checkout $TARGET_REV
