#!/bin/bash

TARGET_REV="e48bc2434bc2d15fcec7f496245726a6a35ca000"

if ! which git
then
	echo "[Error] git not found. Please install it."
	exit 1
fi

if [ -d cloudsuite ]
then
	pushd cloudsuite
	if [ $TARGET_REV == $(git rev-parse HEAD) ]
	then
		echo "Already fetched."
		exit 0
	else
		echo "cloudsuite directory should be removed first."
		exit 1
	fi
fi

# Because official cloudsuite is updated often, we use a fork.
git clone https://github.com/sjp38/cloudsuite-personal.git cloudsuite
pushd cloudsuite
git checkout $TARGET_REV
