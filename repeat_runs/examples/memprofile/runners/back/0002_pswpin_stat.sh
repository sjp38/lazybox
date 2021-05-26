#!/bin/bash

while :
do
	grep pswpin /proc/vmstat >> "$1/pswpin"
	sleep 1
done
