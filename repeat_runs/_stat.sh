#!/bin/bash

BINDIR=`dirname $0`
source $BINDIR/__common.sh

if [ $# -lt 2 ]
then
	echo "Usage: $0 <experiment dir> <path to raw output directories>"
	exit 1
fi

if [ -z $statists_dir ]
then
	statists_dir=$1'/statists/'
fi

echo $2
raw_input_dirs=`ls $2 | grep -e '[0-9][0-9]'`
if [ -z "$raw_input_dirs" ]
then
	echo "no raw input dir in $2"
	exit 1
fi
parsed_dirs=""
for rd in $raw_input_dirs
do
	parsed_dirs+=$2/$rd"/$PARSED "
done
parsed_dir_1=`echo $parsed_dirs | awk '{print $1}'`

stat_odir=$2'/stat/'
mkdir -p $stat_odir

for parsed_file in `ls $parsed_dir_1`
do
	echo $parsed_dir_1 $parsed_file
	statists=`ls $statists_dir | grep -e '^'$parsed_file'*'`
	for statist in $statists
	do
		$statists_dir/$statist $stat_odir $parsed_dirs
	done
done
