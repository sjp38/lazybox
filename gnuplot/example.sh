#!/bin/bash

ODIR="example_plots"
mkdir -p $ODIR

OPTS="--size 7,3 --title 'example' \
	--xrange [0:10] --yrange [0:*] --ylog --xtics_rotate -45 \
	--gnuplot_cmds"

./scatter_datgen.py | ./plot.py $ODIR/scatter.pdf $OPTS \
	--font 'times new roman,20' \
&& \
./scatter-yerr_datgen.py | ./plot.py $ODIR/scatter-yerr.pdf \
	--type scatter-yerr $OPTS --xlog --xtitle "examle x title" \
&& \
./clustered_box_datgen.py | ./plot.py $ODIR/cluster.pdf \
	--type clustered_boxes $OPTS --ytitle "example y title" \
&& \
./clustered_box-yerr_datgen.py | ./plot.py $ODIR/cluster-yerr.pdf \
	--type clustered_boxes-yerr $OPTS
