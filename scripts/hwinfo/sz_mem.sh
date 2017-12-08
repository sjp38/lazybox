#!/bin/bash

sz=`grep "^MemTotal:" /proc/meminfo | awk '{print $2}'`
unit=KiB

if [ $sz -gt 1024 ]
then
	sz=$((sz / 1024))
	unit=MiB
fi

if [ $sz -gt 1024 ]
then
	sz=$((sz / 1024))
	unit=GiB
fi

echo $sz $unit
