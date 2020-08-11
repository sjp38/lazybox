#!/bin/bash

BINDIR=$(dirname "$0")
cd "$BINDIR" || exit 1

if [ -f ebizzy-0.3/ebizzy ]
then
	echo "ebizzy-0.3 directory already exists!"
	exit 1
fi

wget http://www.phoronix-test-suite.com/benchmark-files/ebizzy-0.3.tar.gz
tar xvf ebizzy-0.3.tar.gz
cd ebizzy-0.3 || exit 1
cc -pthread -lpthread -O3 -o ebizzy ebizzy.c
