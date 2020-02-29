#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import tempfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stdin', '-s', action='store_true',
            help='read data from stdin')
    parser.add_argument('--file', '-f', metavar='<file>', help='data file')
    parser.add_argument('--type', '-t', choices=['scatter', 'clustered_boxes'],
            default='scatter', help='plot type')
    parser.add_argument('--ytitle', '-y', metavar='<title>',
            help='y axis title')
    parser.add_argument('--xtitle', '-x', metavar='<title>',
            help='x axis title')
    parser.add_argument('--xlog', action='store_true',
            help='plot x axis in logscale')
    parser.add_argument('--ylog', action='store_true',
            help='plot y axis in logscale')
    parser.add_argument('out', metavar='<file>', help='output file')
    args = parser.parse_args()

    if not args.stdin and not args.file:
        print('no data source specified')

    output = args.out
    out_extension = output.split('.')[-1]
    if not out_extension in ['pdf', 'jpeg', 'png', 'svg']:
        print("Unuspported output type '%s'." % out_extension)
        exit(-1)

    plot_type = args.type

    if args.stdin:
        f = sys.stdin
    elif args.file:
        f = open(args.file, 'r')

    tmp_path = tempfile.mkstemp()[1]
    data_file = open(tmp_path, 'w')

    data = f.read()
    data_file.write(data)
    data_file.close()

    nr_cols = len(data.split('\n')[0].split())
    nr_recs = len(data.split('\n\n')) - 1

    cmdlines = []
    cmdlines.append("""
    load "lzstyle.gp";

    set autoscale;""")

    if plot_type == 'clustered_boxes':
        cmdlines.append("""
        set style data histogram;
        set style histogram cluster gap 2;""")

    cmdlines.append("""
    set term %s;
    set output '%s';
    """ % (out_extension, output))
    if args.xtitle:
        cmdlines.append("set xlabel '%s';" % args.xtitle)
    if args.ytitle:
        cmdlines.append("set ylabel '%s';" % args.ytitle)

    log = ''
    if args.xlog:
        log += 'x'
    if args.ylog:
        log += 'y'
    if log:
        cmdlines.append("set logscale %s;" % log)

    if plot_type == 'scatter':
        cmdlines.append("""
        plot for [idx=0:%s] '%s' index idx using 1:2 with linespoints title columnheader(1);
        """ % (nr_recs, tmp_path))
    elif plot_type == 'clustered_boxes':
        cmdlines.append("""
        plot '%s' using 2:xtic(1) title column, for [i=3:%s] '' using i title column;
        """ % (tmp_path, nr_cols))

    gnuplot_cmd = '\n'.join(cmdlines)

    subprocess.call(['gnuplot', '-e', gnuplot_cmd])
    os.remove(tmp_path)

if __name__ == '__main__':
    main()
