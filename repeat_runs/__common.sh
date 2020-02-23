#!/bin/bash

LBX='../'
ODIR_ROOT='results'

if [ -z "$CURRENT_VARIANT" ]
then
	CURRENT_VARIANT="orig"
fi

if [ -z "$REPEATS" ]
then
	REPEATS=1
fi
