#!/bin/bash

FILE=$1

STARTLINE=`grep --text -n "BUILD SUCCESSFUL" $FILE | cut -f1 -d:`
STARTLINE=$(($STARTLINE + 2))
tail -n +$STARTLINE $FILE
