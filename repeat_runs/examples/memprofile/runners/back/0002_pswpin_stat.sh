#!/bin/bash

while :
do
	cat /proc/vmstat | grep pswpin >> $1/pswpin;
	sleep 1;
done
