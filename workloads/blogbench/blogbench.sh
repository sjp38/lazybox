#!/bin/bash

WORKING_DIR=`dirname $0`
RUN_DIR="run_dir"

pushd $WORKING_DIR

which blogbench
if [ $? != 0 ]
then
	echo "[error] blogbench not installed"
	popd
	exit 1
fi

if [ ! -d $RUN_DIR ]
then
	mkdir $RUN_DIR
fi

blogbench -d $WORKING_DIR/$RUN_DIR

popd
