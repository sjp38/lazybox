#!/bin/bash

# Make lazybox experiment configuration for given workload/variance.  Users can
# pipe the generated configuration to the `run_exps.py` for actual run of the
# experiment.

BINDIR=`dirname $0`

source $BINDIR/__common.sh

if [ $# -ne 2 ]
then
	echo "USAGE: $0 <expname> <variance>"
	exit 1
fi


EXPNAME=$1
VARIANCE=$2

ODIR=$ODIR_ROOT/$EXPNAME/$VARIANCE

MAX_REPEAT=10
for (( unqid=1; unqid <= $MAX_REPEAT; unqid+=1 ))
do
	CANDIDATE=$ODIR/`printf "%02d" $unqid`
	if [ ! -d $CANDIDATE ]
	then
		ODIR=$CANDIDATE
		break
	fi
	if [ $unqid -eq $MAX_REPEAT ]
	then
		echo "[Error] $MAX_REPEAT repeated results already exists!!!"
		exit 1
	fi
done
mkdir -p $ODIR

runners_dir=$EXPNAME/runners
for work_types in start main back end
do
	pattern='^'$work_types'_*'
	runners=`ls $runners_dir | grep -e $pattern | sort`
	for runner in $runners
	do
		echo "$work_types" $runners_dir/$runner $ODIR
	done
done
GROUP=`groups $USER | awk '{print $3}'`
echo "end chown -R $USER:$GROUP $ODIR_ROOT"
