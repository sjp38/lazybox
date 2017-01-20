#!/bin/bash

if [ $# -ne 1 ];
then
	echo "Usage: $0 <target>"
	exit 1
fi

TARGET=$1
BOOTS_DIR=/home/sjpark/boots

pushd $BOOTS_DIR
cp -R $TARGET/* /
sync
popd
