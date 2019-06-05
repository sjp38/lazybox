load "lzstyle.gp"

set autoscale

set term pdf font "times new roman,12" size 3,3
set output "plot.pdf"

if (!exists("DATA") || !exists("NR_IDXS")) {
	print "DATA and NR_IDXS should be passed via -e option."
	print "(e.g., \`$ gnuplot -e \"DATA='./data'; NR_IDXS='3'\" ./example.gp\`)"
	exit
}

set xlabel XLABEL
set ylabel YLABEL

if (LOGSCALE ne "") {
	set yrange [0.1:*]
}

if (LOGSCALE eq "x") {
	set logscale x
}

if (LOGSCALE eq "y") {
	set logscale y
}

if (LOGSCALE eq "xy") {
	set logscale xy
}

plot								\
	DATA using 1:2:3 linestyle 1 with yerrorbars notitle,	\
	for [IDX=0:NR_IDXS] DATA index IDX using 1:2		\
		with linespoints title columnheader(1)		\
