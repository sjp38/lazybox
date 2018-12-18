#!/bin/bash

if [ -d mosbench ]
then
	echo "mosbench directory already exists!"
	exit 1
fi

git clone https://github.com/sjp38/mosbench
