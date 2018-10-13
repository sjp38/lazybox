#!/bin/bash

# Install ply

BINDIR=`dirname $0`
cd $BINDIR

git clone https://github.com/iovisor/ply.git
cd ply
