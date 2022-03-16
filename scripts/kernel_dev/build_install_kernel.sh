#!/bin/bash

set -e

if [ $# -ne 3 ]
then
	echo "Usage: $0 <src dir> <build dir> <config file to append>"
	exit 1
fi

bindir=$(dirname "$0")
src_dir=$1
build_dir=$2
additional_config_file=$3

orig_config=$build_dir/.config

if [ ! -d "$build_dir" ]
then
	mkdir "$build_dir"
fi

if [ ! -f "$orig_config" ]
then
	cp "/boot/config-$(uname -r)" "$orig_config"
fi

cat "$additional_config_file" >> "$build_dir/.config"
make -C "$src_dir" O="$build_dir" olddefconfig
make -C "$src_dir" O="$build_dir" -j$(nproc)
sudo make -C "$src_dir" O="$build_dir" modules_install install
kernelversion=$(make -C "$src_dir" O="$build_dir" -s kernelrelease)
sudo "$bindir/set_kernel.py" "$kernelversion"
