load "lzstyle.gp"

set autoscale

set auto x
set yrange [0:*]

set style data histogram
set style histogram cluster gap 2

set term pdf font "times new roman,12"
set output "plot.pdf"

if (!exists("DATA") || !exists("NR_COLS")) {
	print "DATA and NR_COLS should be passed via -e option."
	print "(e.g., \`$ gnuplot -e \"DATA='./data'; NR_COLS='3'\" ./example.gp\`)"
	exit
}

plot DATA using 2:xtic(1) title column,	\
	for [i=3:NR_COLS] '' using i title column
