#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import tempfile

def get_args():
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
    return parser.parse_args()

def gen_gp_cmd(data_path, nr_recs, nr_cols, plot_type, out_extension, output,
        xtitle, ytitle, xlog, ylog):
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
    if xtitle:
        cmdlines.append("set xlabel '%s';" % xtitle)
    if ytitle:
        cmdlines.append("set ylabel '%s';" % ytitle)

    log = ''
    if xlog:
        log += 'x'
    if ylog:
        log += 'y'
    if log:
        cmdlines.append("set logscale %s;" % log)

    if plot_type == 'scatter':
        cmdlines.append("""
        plot for [idx=0:%s] '%s' index idx using 1:2 with linespoints title columnheader(1);
        """ % (nr_recs, data_path))
    elif plot_type == 'clustered_boxes':
        cmdlines.append("""
        plot '%s' using 2:xtic(1) title column, for [i=3:%s] '' using i title column;
        """ % (tmp_path, nr_cols))

    return '\n'.join(cmdlines)

def main():
    args = get_args()

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
    data = f.read()
    f.close()

    tmp_path = tempfile.mkstemp()[1]
    with open(tmp_path, 'w') as f:
        f.write(data)

    nr_cols = len(data.split('\n')[0].split())
    nr_recs = len(data.split('\n\n')) - 1

    gnuplot_cmd = gen_gp_cmd(tmp_path, nr_recs, nr_cols, plot_type,
            out_extension, output, args.xtitle, args.ytitle, args.xlog,
            args.ylog)

    subprocess.call(['gnuplot', '-e', gnuplot_cmd])
    os.remove(tmp_path)

if __name__ == '__main__':
    main()
