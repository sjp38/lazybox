#!/bin/bash

echo "Dev	MAC			Driver	State"

for e in /sys/class/net/*
do
	dev=`basename $e`
	driver=`readlink $e/device/driver/module`
	if [ $driver ]
	then
		driver=`basename $driver`
	else
		driver="none"
	fi
	addr=`cat $e/address`
	operstate=`cat $e/operstate`

	printf "$dev\t$addr\t$driver\t$operstate\n"
done
