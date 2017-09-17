load "lzstyle.gp"

set autoscale

set key tmargin center
set key horizontal
set key box

set term pdf font "times new roman,12"
set output "plot.pdf"

if (!exists("DATA") || !exists("NR_IDXS")) {
	print "DATA and NR_IDXS should be passed via -e option."
	print "(e.g., \`$ gnuplot -e \"DATA='./data'; NR_IDXS='3'\" ./example.gp\`)"
	exit
}

set xlabel XLABEL
set ylabel YLABEL

if (LOGSCALE eq "x") {
	set logscale x
}

if (LOGSCALE eq "y") {
	set logscale y
}

if (LOGSCALE eq "xy") {
	set logscale xy
}

plot 							\
	for [IDX=0:NR_IDXS] DATA index IDX using 1:2 	\
		with linespoints title columnheader(1)
