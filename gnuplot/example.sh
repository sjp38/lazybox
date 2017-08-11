#!/bin/bash

gnuplot -e "DATA='./example.dat'" ./example.gp && \
	evince plot.pdf && rm plot.pdf
