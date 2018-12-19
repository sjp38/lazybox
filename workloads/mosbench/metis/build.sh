#!/bin/bash

BINDIR=`dirname $0`
cd $BINDIR

if [ ! -d ../mosbench/metis ]
then
	echo "source code for metis is not found."
	exit 1
fi

if ! dpkg -l | grep -q libnuma-dev
then
	echo "libnuma-dev package is not installed"
	exit 1
fi

make -C ../mosbench/metis
