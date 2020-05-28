#!/bin/bash

# Install ply

BINDIR=$(dirname "$0")
pushd "$BINDIR" > /dev/null

git clone https://github.com/iovisor/ply.git
