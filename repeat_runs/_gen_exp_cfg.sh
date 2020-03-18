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

exp_basename=`basename $EXPNAME`
ODIR=$ODIR_ROOT/$exp_basename/$VARIANCE

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
for runner_type in "start" "main" "back" "end"
do
	custom_runners_varname=$runner_type"_RUNNERS"
	for runner in ${!custom_runners_varname}
	do
		echo "$runner_type $runner $ODIR"
	done

	runners_dir=$EXPNAME/runners/$runner_type
	if [ ! -d $runners_dir ]
	then
		continue
	fi
	for runner in `ls $runners_dir | sort`
	do
		echo "$runner_type" $runners_dir/$runner $ODIR
	done
done
GROUP=`groups $USER | awk '{print $3}'`
echo "end chown -R $USER:$GROUP $ODIR_ROOT"
