#!/bin/bash

if [ $# -ne 1 ]
then
	echo "USAGE: $0 <run-webserving.sh output file>"
	exit 1
fi

FILE=$1

STARTLINE=`grep --text -n "BUILD SUCCESSFUL" $FILE | cut -f1 -d:`
STARTLINE=$(($STARTLINE + 2))
tail -n +$STARTLINE $FILE | head -n -1
