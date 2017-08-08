#!/bin/bash

FILEDIR=`dirname $0`

pushd $FILEDIR
./cleanup-webserving.sh
./setup-webserving.sh

# Wait for mysql startup
# TODO: Wait more gracefully
echo "Wait mysql startup..."
for i in {1..5}
do
	echo $i
	sleep 1
done

./run-webserving.sh $1
popd
