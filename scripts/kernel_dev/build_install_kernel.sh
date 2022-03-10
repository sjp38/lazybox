#!/bin/bash

if [ $# -ne 3 ]
then
	echo "Usage: $0 <src dir> <build dir> <config file to append>"
	exit 1
fi

bindir=$(dirname "$0")
src_dir=$1
build_dir=$2
config_file=$3

cat "$config_file" >> "$build_dir/.config"
make -C "$src_dir" O="$build_dir" olddefconfig
make -C "$src_dir" O="$build_dir" -j$(nproc)
sudo make -C "$src_dir" O="$build_dir" modules_install install
kernelversion=$(make -C "$src_dir" kernelversion | tail -n 2 | head -n 1)
sudo "$bindir/set_kernel.py" "$kernelversion"
