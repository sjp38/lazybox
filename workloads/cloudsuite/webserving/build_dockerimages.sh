#!/bin/bash

WORKING_DIR=`dirname $0`

pushd $WORKING_DIR/../

if [ ! -d cloudsuite ]
then
	echo "Fetch cloudsuite source code first"
	exit 1
fi

REPONAME="lb-cloudsuite/web-serving"

pushd ./cloudsuite/benchmarks/web-serving/db_server
docker build -t $REPONAME:mysql ./

pushd ../memcached_server
docker build -t $REPONAME:memcached ./

pushd ../web_server
docker build -t $REPONAME:webserver ./

pushd ../faban_client
docker build -t $REPONAME:client ./
