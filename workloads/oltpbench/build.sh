#!/bin/bash

BINDIR=`dirname $0`
pushd $BINDIR

if [ ! -d src ]
then
	echo "Source code is not exists.  Fetch it..."
	./fetch-src.sh
fi

cd src/
ant

popd
