#!/bin/bash

if ! which git
then
	echo "[Error] git not found. Please install it."
	exit 1
fi

# Because official cloudsuite is updated often, we use a fork.
git clone https://github.com/sjp38/cloudsuite-personal.git cloudsuite
