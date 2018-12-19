#!/bin/bash

if [ -d mosbench ]
then
	echo "mosbench directory already exists!"
	exit 1
fi

git clone https://github.com/sjp38/mosbench
cd mosbench
# Check out latest version as of 19 Dec 2018.
git checkout c250c395fab356ab83413db43bf9844cb4f63d4f	# Mar 4 2013
