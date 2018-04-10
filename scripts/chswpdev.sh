#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <new swap device>"
	exit 1
fi

SWPDEV=$1

sudo swapoff -a
sudo swapon $SWPDEV
