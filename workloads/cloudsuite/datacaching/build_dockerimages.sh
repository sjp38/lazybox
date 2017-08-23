#!/bin/bash

WORKING_DIR=`dirname $0`

pushd $WORKING_DIR/../

if [ ! -d cloudsuite ]
then
	echo "Fetch cloudsuite source code first"
	exit 1
fi

REPONAME="lb-cloudsuite/data-caching"

pushd ./cloudsuite/benchmarks/data-caching/server
docker build -t $REPONAME:server ./

pushd ../client
docker build -t $REPONAME:client ./
