#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 <delay> <count>"
	exit 1
fi

delay=$1
count=$2

for ((i = 0; i != count; i++))
do
	read -r cpu user nice system idle iowait irq softirq steal \
		guest guest_nice < /proc/stat
	if [ "$cpu" != "cpu" ]
	then
		echo "/proc/stat has unexpected format"
		exit 1
	fi
	old_active=$((user + nice + system + irq + softirq + steal + \
		guest + guest_nice))
	old_total=$((old_active + idle + iowait))

	sleep "$delay"

	read -r cpu user nice system idle iowait irq softirq steal \
		guest guest_nice < /proc/stat
	if [ "$cpu" != "cpu" ]
	then
		echo "/proc/stat has unexpected format"
		exit 1
	fi
	now_active=$((user + nice + system + irq + softirq + steal + \
		guest + guest_nice))
	now_total=$((now_active + idle + iowait))

	total=$((now_total - old_total))
	active=$((now_active - old_active))

	# percent
	echo $SECONDS $((active * 100 / total))
done
