#!/bin/bash

grep "model name" /proc/cpuinfo | head -n 1 | awk '{
	for (i=4; i <NF + 1; i++) {
		printf $i
		if (i != NF) {
			printf " "
		}
	}
	printf "\n"
}'
