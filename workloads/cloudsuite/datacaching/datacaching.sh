#!/bin/bash

BINDIR=`dirname $0`
pushd $BINDIR

./cleanup.sh
./startserver.sh

docker run -d --name dc-client --net caching_network \
	lb-cloudsuite/data-caching:client \
	/bin/sh -c "while true; do sleep 3; done"

WORKDIR=/usr/src/memcached/memcached_client
DATADIR=/usr/src/memcached/twitter_dataset

docker exec dc-client \
	/bin/bash -c "echo 'dc-server, 11211' > $WORKDIR/docker_servers.txt"

# warmup
docker exec dc-client \
	$WORKDIR/loader \
	-a $DATADIR/twitter_dataset_unscaled \
	-o $DATADIR/twitter_dataset_100x	\
	-s $WORKDIR/docker_servers.txt -w 4 -S 100 -D 10240 -j -T 2

# run
docker exec dc-client \
	$WORKDIR/loader \
	-a $DATADIR/twitter_dataset_100x \
	-s $WORKDIR/docker_servers.txt -g 0.8 -T 1 -c 20 -w 6 -t 180


popd
