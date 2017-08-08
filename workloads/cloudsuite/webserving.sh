#!/bin/bash

FILEDIR=`dirname $0`

pushd $FILEDIR
./cleanup-webserving.sh
./setup-webserving.sh

# Wait for mysql startup
# TODO: Wait more gracefully
sleep 5

./run-webserving.sh
popd
