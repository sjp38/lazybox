#!/bin/bash

BINDIR=$(dirname "$0")
cd "$BINDIR" || exit 1

if [ ! -f ../mosbench/metis/obj/app/wrmem ]
then
	echo "the execution file for the metis is not found."
	exit 1
fi

if [ $# -ne 1 ]
then
	echo "Usage: $0 <number of cores>"
	exit 1
fi

NR_CORES=$1

(time ../mosbench/metis/obj/app/wrmem -p "$NR_CORES") 2>&1
