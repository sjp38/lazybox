#!/bin/bash

set -e

ODIR="example_plots"
mkdir -p $ODIR

OPTS="--size 7,3 --title 'example' "
OPTS+="--xrange [0:10] --yrange [0:*] --ylog --xtics_rotate -45 "
OPTS+="--gnuplot_cmds"

OPTS=($OPTS)

./scatter_datgen.py | ./plot.py $ODIR/scatter.pdf "${OPTS[@]}" \
	--font 'times new roman,20'

./scatter-yerr_datgen.py | ./plot.py $ODIR/scatter-yerr.pdf \
	--type scatter-yerr "${OPTS[@]}" --xlog --xtitle "examle x title"

./clustered_box_datgen.py | ./plot.py $ODIR/cluster.pdf \
	--type clustered_boxes "${OPTS[@]}" --ytitle "example y title"

./clustered_box-yerr_datgen.py | ./plot.py $ODIR/cluster-yerr.pdf \
	--type clustered_boxes-yerr "${OPTS[@]}"

echo
echo "stdout plots"

./scatter_datgen.py | ./plot.py stdout > "$ODIR/scatter_stdout"
./clustered_box_datgen.py | ./plot.py stdout --data_fmt table \
	> "$ODIR/clustered_box_stdout"

./scatter_datgen.py --max 10000000000 \
	| ./plot.py stdout --stdout_val_type bytes \
	> "$ODIR/scatter_stdout_bytes"
./scatter_datgen.py | ./plot.py stdout --stdout_val_type seconds \
	> "$ODIR/scatter_stdout_seconds"

echo
echo "check the outputs in $ODIR"
