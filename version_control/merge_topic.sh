#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 <baseline> <topic>"
	exit 1
fi

baseline="$1"
topic="$2"

head_commit=$(git rev-parse HEAD)
git reset --hard "$baseline"
git merge "$head_commit" --no-ff --no-edit -m "Merge \"$topic\""
