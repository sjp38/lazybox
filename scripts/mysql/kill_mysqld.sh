#!/bin/bash

BINDIR=$(dirname "$0")

pushd "$BINDIR" > /dev/null

sudo -u mysql kill -SIGTERM "$(pidof mysqld)"

../wait_workof.sh mysqld

popd > /dev/null
