#!/bin/bash

DEBUGFS_DIR="/sys/kernel/debug/gcma"
FILES_FILE="files"
TMP_DIR="/tmp"

if [ ! -d $DEBUGFS_DIR ]; then
	echo "gcma debugfs not exist"
	exit 1
fi

ls $DEBUGFS_DIR > $TMP_DIR/$FILES_FILE

while read FILE;
do
	echo $FILE
	cat $DEBUGFS_DIR/$FILE
	echo ""
done <$TMP_DIR/$FILES_FILE	

rm $TMP_DIR/$FILES_FILE
