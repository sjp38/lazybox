#!/bin/bash

if ! perf probe --list | grep lb:swpout > /dev/null
then
	echo "Add swpout probe"
	perf probe --add lb:swpout='__swap_writepage page' &> /dev/null
fi
if ! perf probe --list | grep lb:swpin > /dev/null
then
	echo "Add swpin probe"
	perf probe --add lb:swpin='swap_readpage page' &> /dev/null
fi

echo "Start tracing"
if [ $# -eq 1 ]
then
	additionaloption=$1
fi
perf record -e lb:swpin -e lb:swpout "$additionaloption"
