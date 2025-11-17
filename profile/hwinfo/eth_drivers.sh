#!/bin/bash

echo "Dev	MAC			Driver	State"

for e in /sys/class/net/*
do
	dev=$(basename "$e")
	driver=$(readlink "$e"/device/driver/module)
	if [ "$driver" ]
	then
		driver=$(basename "$driver")
	else
		driver="none"
	fi
	addr=$(cat "$e/address")
	operstate=$(cat "$e/operstate")

	printf "%s\t%s\t%s\t%s\n" "$dev" "$addr" "$driver" "$operstate"
done
