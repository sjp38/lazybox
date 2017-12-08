#!/bin/bash

if ! which lspci > /dev/null
then
	echo "[ERROR] You should install lspci"
	exit 1
fi

function ethernets() {
	lspci | grep "Ethernet controller" | awk '{
		for (i = 2; i <= NF; i++) {
			printf $i
			if (i < NF) {
				printf " "
			}
		}
		printf "\n"
	}' | uniq
}

IFS=$'\n'
for l in `ethernets`
do
	echo $l x `lspci | grep $l | wc -l`
done
