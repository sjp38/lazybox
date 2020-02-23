#!/bin/bash

BINDIR=`dirname $0`

LBX=$BINDIR'/../'
ODIR_ROOT=$PWD'/results'

if [ -z "$CURRENT_VARIANT" ]
then
	CURRENT_VARIANT="orig"
fi

if [ -z "$REPEATS" ]
then
	REPEATS=1
fi
