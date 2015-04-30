#!/bin/bash

WORKING_DIR=`dirname $0`

pushd $WORKING_DIR

DATA_FILE="2000MiB_file"
STRESS_FILE="stress"

if [ ! -f $DATA_FILE ]
then
	echo "$DATA_FILE not found. create it."
	dd if=/dev/zero of=$DATA_FILE bs=1M count=2000
fi

make
./stress 600

popd
