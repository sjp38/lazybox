#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <size of zram device>"
	exit 1
fi

ZRAM_SIZE=$1
NR_CPUS=$(grep -c processor /proc/cpuinfo)

modprobe zram
echo 1 > /sys/block/zram0/reset
echo "$NR_CPUS" > /sys/block/zram0/max_comp_streams
echo "$ZRAM_SIZE" > /sys/block/zram0/disksize

swapoff -a
mkswap /dev/zram0
swapon /dev/zram0
echo "zram swap ($ZRAM_SIZE) enabled"
