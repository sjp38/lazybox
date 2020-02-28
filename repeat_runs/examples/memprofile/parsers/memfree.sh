#!/bin/bash

LBX=$HOME/lazybox

$LBX/scripts/report/memfree_to_used.py $1/memfree > $2/memused

MFTOT=0
NR_MF=0
for mf in `awk '{print $2}' $2/memused`
do
	MFTOT=$(($MFTOT + $mf))
	NR_MF=$(($NR_MF + 1))
done
echo "memused.avg: " $(($MFTOT / $NR_MF)) > $2/memused.avg
