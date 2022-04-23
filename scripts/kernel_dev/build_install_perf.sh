#!/bin/bash

set -e

if [ $# -ne 2 ]
then
	echo "Usage: <linux dir> <perf build dir>"
	exit 1
fi

perf_file="/usr/bin/perf"

if [ -f "$perf_file" ]
then
	echo "$perf_file already exists"
	exit 1
fi

linux_dir=$1
perf_build_dir=$2
perf_dir="$linux_dir/tools/perf"

sudo apt install -y build-essential libdw-dev systemtap-sdt-dev libunwind-dev \
		libslang2-dev libperl-dev python-dev libiberty-dev liblzma-dev \
		libzstd-dev libcap-dev libnuma-dev libbabeltrace-ctf-dev

make -C "$perf_dir" O="$perf_build_dir"
make -C "$perf_dir" O="$perf_build_dir" install
sudo ln -s "$HOME/bin/perf" "$perf_file"
