#!/bin/bash

BINDIR=`dirname $0`

LBX=$BINDIR'/../'
ODIR_ROOT=$PWD'/results'

if [ -z "$CFG" ]
then
	CFG=$BINDIR/examples/example.config
fi

source $CFG

if [ -z "$VARIANTS" ]
then
	VARIANTS="orig"
fi

if [ -z "$REPEATS" ]
then
	REPEATS=1
fi

PARSED='parsed'
