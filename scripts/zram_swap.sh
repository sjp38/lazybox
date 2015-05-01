#!/bin/bash

echo $#

if [ $# -ne 1 ]
then
	echo "Illegal number of parameters."
	echo "usage: $0 <size of zram device>"
	exit 1
fi

ZRAM_SIZE=$1
NR_CPUS=`cat /proc/cpuinfo | grep -c processor`

modprobe zram
echo 1 > /sys/block/zram0/reset
echo $NR_CPUS > /sys/block/zram0/max_comp_streams
echo $ZRAM_SIZE > /sys/block/zram0/disksize

swapoff -a
mkswap /dev/zram0
swapon /dev/zram0
echo "zram swap ($ZRAM_SIZE) enabled"
