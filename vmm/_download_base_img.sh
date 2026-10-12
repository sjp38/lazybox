#!/bin/bash
# SPDX-License-Identifier: GPL-2.0

set -e

if [ $# -ne 2 ]
then
	echo "Usage: $0 <debian13> <output path>"
	echo "E.g., $0 debian13 base.img"
	exit 1
fi

target=$1
output_path=$2

case "$target" in
	debian13)
		link=https://cloud.debian.org/images/cloud/trixie/latest/debian-13-generic-amd64.qcow2
		;;
	*)
		;;
esac

curl -L -o "$output_path" "$link"
