#!/bin/bash

BINDIR=`dirname $0`

LBX=$BINDIR'/../'
ODIR_ROOT=$PWD'/results'

VARIANTS="orig"
REPEATS=1
PARSED='parsed'

if [ -z "$CFG" ]
then
	CFG=$BINDIR/examples/example.config
fi

source $CFG

if [ "$1" ]
then
	EXPERIMENTS=$1
fi
