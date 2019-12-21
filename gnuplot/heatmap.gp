load "lzstyle.gp"

set autoscale

set term pdf font "times new roman,12" size 3,3
set output "plot.pdf"

if (!exists("DATA")) {
	print "DATA should be passed via -e option."
	print "(e.g., \`$ gnuplot -e \"DATA='./data'\" ./heatmap.gp\`)"
	exit
}

set xlabel XLABEL
set ylabel YLABEL

plot DATA using 1:2:3 with image title ""
