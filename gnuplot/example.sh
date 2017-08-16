#!/bin/bash

gnuplot -e "DATA='./example.dat'; NR_IDXS='2'" ./example.gp && \
	evince plot.pdf && rm plot.pdf
