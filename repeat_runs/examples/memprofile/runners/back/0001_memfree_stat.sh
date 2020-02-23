#!/bin/bash

while :
do
	cat /proc/meminfo | grep MemFree >> $1/memfree;
	sleep 1;
done
