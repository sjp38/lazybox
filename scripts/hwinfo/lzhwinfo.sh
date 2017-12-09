#!/bin/bash

BINDIR=`dirname $0`

pushd $BINDIR > /dev/null

MODEL=`./cpumodel.sh`
SOCKS=`./nr_cpusocks.sh`
CORES=`./nr_cpuspersock.sh`
THRS=`./nr_thrspercpu.sh`
TOTAL_THRS=`./nr_hwthrs.sh`

DETAIL="$TOTAL_THRS thrs / $SOCKS socks / $CORES cores / $THRS hyper-thr"
echo CPU: $MODEL "($DETAIL)"
echo MEM: `./sz_mem.sh`

function linestocsv() {
	IFS=$'\n'
	RES=""
	for l in $1
	do
		RES=$RES$l", "
	done
	if [ $RES ]
	then
		echo "${RES::-2}"
	fi
	unset IFS
}

printf "NICs: "
linestocsv "`./nics.sh`"
printf "IPs: "
linestocsv "`./ipaddrs.sh`"
printf "STORAGEs: "
linestocsv "`./blockdevs.sh`"

popd > /dev/null
