#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <backup location>"
	exit 1
fi

BACKUP=$1
MYSQLDATA=/usr/local/mysql/data

sudo cp -R $MYSQLDATA $BACKUP
sync
