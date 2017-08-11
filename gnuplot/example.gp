load "lzstyle.gp"

set autoscale fix

set key tmargin center
set key horizontal
set key box

set term pdf font "times new roman,12"
set output "plot.pdf"

# DATA is data file name.  It should be passed from shell via -e option.
if (!exists("DATA")) {
	print "DATA variable should be passed via -e option."
	print "(e.g., $ gnuplot -e \"DATA='./filename'\" ./example.gp)"
	exit
}

plot for [IDX=0:2] DATA index IDX using 1:2 \
	with linespoints title columnheader(1)
