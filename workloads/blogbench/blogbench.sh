#!/bin/bash

WORKING_DIR=`dirname $0`
WORK_DIR="blogbenchdir"

pushd $WORKING_DIR

which blogbench
if [ $? != 0 ]
then
	echo "[error] blogbench not installed"
	popd
	exit 1
fi

blogbench -d $WORK_DIR

popd
