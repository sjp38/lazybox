#!/bin/bash

for CONT in faban_client web_server memcache_server mysql_server
do
	docker rm -f $CONT
done
