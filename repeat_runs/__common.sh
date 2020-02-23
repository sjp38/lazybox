#!/bin/bash

LBX='../'

if [ -z "$CURRENT_VARIANT" ]
then
	CURRENT_VARIANT="orig"
fi

if [ -z "$REPEATS" ]
then
	REPEATS=1
fi
