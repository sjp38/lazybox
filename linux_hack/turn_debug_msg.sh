#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 <files> <on|off>"
	exit 1
fi

files=$1
onoff=$2

cmd="file $files"
if [ "$onoff" = "on" ]
then
	cmd+=" +p"
else
	cmd=" -p"
fi

echo -n "$cmd" | sudo tee /sys/kernel/debug/dynamic_debug/control
echo ""
