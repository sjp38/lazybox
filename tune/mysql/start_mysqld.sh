#!/bin/bash

BINDIR=$(dirname "$0")

pushd "$BINDIR" > /dev/null

sudo -u mysql /usr/local/mysql/bin/mysqld_safe --user=mysql &

./wait_workof.sh mysqld

popd > /dev/null
