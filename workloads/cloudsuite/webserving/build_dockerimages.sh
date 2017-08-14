#!/bin/bash

WORKING_DIR=`dirname $0`

pushd $WORKING_DIR/../

if [ ! -d cloudsuite ]
then
	echo "Fetch cloudsuite source code first"
	exit 1
fi

pushd ./cloudsuite/benchmarks/web-serving/db_server
docker build -t sj-cloudsuite/web-serving:mysql ./

pushd ../memcached_server
docker build -t sj-cloudsuite/web-serving:memcached ./

pushd ../memcached_server
docker build -t sj-cloudsuite/web-serving:webserver ./

pushd ../faban_client
docker build -t sj-cloudsuite/web-serving:client ./
