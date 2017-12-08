#!/bin/bash

BINDIR=`dirname $0`

pushd $BINDIR > /dev/null

NR_THRS=`./nr_hwthrs.sh`
NR_CPUS=$((`./nr_cpusocks.sh` * `./nr_corespersock.sh`))

echo $(($NR_THRS / $NR_CPUS))
