#!/bin/bash

WORKING_DIR=`dirname $0`
WORK_DIR="blogbenchdir"

pushd $WORKDING_DIR

which blogbench
if [ $? != 0 ]
then
	echo "blogbench not installed"
	exit 1
fi

blogbench -d $WORK_DIR

popd
