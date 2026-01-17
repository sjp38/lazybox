#!/bin/bash

git for-each-ref --sort=creatordate \
	--format '%(creatordate:short) %(refname:short)' refs/tags
