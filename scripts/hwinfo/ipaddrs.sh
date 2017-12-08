#!/bin/bash

ifconfig -a | grep "inet addr" | awk '{
	if ($2 == "addr:127.0.0.1") {
		exit
	}
	print $2
}' | awk -F: '{ print $2 }'
