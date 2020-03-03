#!/bin/bash

ODIR="example_plots"
mkdir -p $ODIR

OPTS="--size 5,1 --title 'example' \
	--xrange [0:10] --yrange [0:*] --ylog --xtics_rotate 45 \
	--gnuplot_cmds"

./scatter_datgen.py | ./plot.py $ODIR/scatter.pdf --stdin $OPTS
./scatter-yerr_datgen.py | ./plot.py $ODIR/scatter-yerr.pdf --stdin \
	--type scatter-yerr $OPTS
./clustered_box_datgen.py | ./plot.py $ODIR/cluster.pdf --stdin \
	--type clustered_boxes $OPTS
./clustered_box-yerr_datgen.py | ./plot.py $ODIR/cluster-yerr.pdf --stdin \
	--type clustered_boxes-yerr $OPTS
