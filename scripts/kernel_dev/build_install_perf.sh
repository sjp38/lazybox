#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: <linux dir> <perf build dir>"
	exit 1
fi

linux_dir=$1
perf_build_dir=$2
perf_dir="$linux_dir/tools/perf"

sudo apt install -y build-essential 

make -C "$perf_dir" O="$perf_build_dir"
make -C "$perf_dir" O="$perf_build_dir" install
sudo ln -s "$HOME/bin/perf" "/usr/bin/perf"
