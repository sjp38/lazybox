#!/bin/bash

if [ $# -lt 2 ];
then
	echo "Usage: $0 <number of iteration> <count of pages to be alloced>"
	echo ""
	exit 1
fi

WORKING_DIR=`dirname $0`

DEBUGFS_ROOT="/sys/kernel/debug"
DEBUGFS=$DEBUGFS"/cma_eval"
NR_CMA_REQ=$1
NR_ALLOC_PAGES="${@:2}"

echo "[[ Test Start ]]"
echo "kernel version: `uname -r`"
echo "kernel param: \"`cat /proc/cmdline`\""
echo "date: `date`"
echo ""

pushd $WORKING_DIR

echo "[before stat]"
./gcma_stat.sh

for i in $(seq 1 $NR_CMA_REQ)
do
	for NR in $NR_ALLOC_PAGES
	do
		sleep 2
		echo $NR > $DEBUGFS_ROOT/cma_eval/eval
	done
done

echo ""
echo "[latency]"
cat $DEBUGFS_ROOT/cma_eval/res

echo ""
echo "[histogram]"
cat $DEBUGFS_ROOT/cma_eval/res.hist

echo ""
echo "[after stat]"
$WORKING_DIR/gcma_stat.sh

popd

echo "[[ Test Done ]]"
