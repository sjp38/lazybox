#!/bin/bash

if ! which lspci > /dev/null
then
	echo "[ERROR] You should install lspci"
	exit 1
fi

lspci | grep "Ethernet controller" | awk '{
	for (i = 4; i <= NF; i++) {
		printf $i
		if (i < NF) {
			printf " "
		}
	}
	printf "\n"
}'
