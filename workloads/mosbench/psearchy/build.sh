#!/bin/bash

BINDIR=$(dirname "$0")
cd "$BINDIR" || exit 1

if [ ! -d ../mosbench/psearchy ]
then
	echo "psearchy source code directory not found."
	exit 1
fi

if ! dpkg -l | grep -q libdb-dev
then
	echo "libdb-dev package is not installed"
	exit 1
fi

make -C ../mosbench/psearchy/mkdb all
