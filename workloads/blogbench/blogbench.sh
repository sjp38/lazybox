#!/bin/bash

WORKING_DIR=$PWD/`dirname $0`
RUN_DIR="run_dir"

pushd $WORKING_DIR

uname -a

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
rm -fr $RUN_DIR/*

blogbench -d $WORKING_DIR/$RUN_DIR

popd
