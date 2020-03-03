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
    parser.add_argument('--type', '-t',
            choices=['scatter', 'scatter-yerr',
                'clustered_boxes', 'clustered_boxes-yerr'],
            default='scatter', help='plot type')
    parser.add_argument('--ytitle', '-y', metavar='<title>',
            help='y axis title')
    parser.add_argument('--xtitle', '-x', metavar='<title>',
            help='x axis title')
    parser.add_argument('--xlog', action='store_true',
            help='plot x axis in logscale')
    parser.add_argument('--ylog', action='store_true',
            help='plot y axis in logscale')
    parser.add_argument('--xtics_rotate', metavar='<degree>', type=int,
            help='xtics rotate degree')
    parser.add_argument('--font', metavar='<font>', help='font and size')
    parser.add_argument('--size', metavar='<width,height>',
            help='size of plotted image')
    parser.add_argument('out', metavar='<file>', help='output file')
    return parser.parse_args()

def gen_gp_cmd(data_path, nr_recs, nr_cols, plot_type, output, xtitle, ytitle,
        xlog, ylog, xtics_rotate, font, size):
    cmds = []
    cmds += ['load "%s/lzstyle.gp";' % os.path.dirname(__file__)]
    cmds += ['set autoscale;']

    if plot_type == 'clustered_boxes':
        cmds += ['set style data histogram;',
        'set style histogram cluster gap 2;']
    elif plot_type == 'clustered_boxes-yerr':
        cmds += ['set style data histogram;',
        'set style histogram cluster gap 2 errorbars;']

    cmd='set term %s noenhanced' % output.split('.')[-1]
    if font:
        cmd += ' font "%s"' % font
    if size:
        cmd += ' size %s' % size
    cmd += ";"
    cmds.append(cmd)

    cmds += ['set output "%s";' % output]

    if xtics_rotate:
        cmds += ['set xtics rotate by %d;' % xtics_rotate]

    if xtitle:
        cmds += ['set xlabel "%s";' % xtitle]
    if ytitle:
        cmds += ['set ylabel "%s";' % ytitle]

    log = ''
    if xlog:
        log += 'x'
    if ylog:
        log += 'y'
    if log:
        cmds += ['set logscale %s;' % log]

    if plot_type == 'scatter-yerr':
        cmds.append("""
        plot "%s" using 1:2:3 linestyle 1 with yerrorbars notitle, \
        for [idx=0:%s] "%s" index idx using 1:2 with linespoints \
                title columnheader(1);
        """ % (data_path, nr_recs, data_path))
    elif plot_type == 'scatter':
        cmds.append("""
        plot for [idx=0:%s] "%s" index idx using 1:2 with linespoints \
                title columnheader(1);
        """ % (nr_recs, data_path))
    elif plot_type == 'clustered_boxes-yerr':
        nr_realcols = (nr_cols - 1) / 2
        cmds.append("""
        plot for [i=2:%d:2] "%s" using i:i+1:xtic(1) title col(i);
        """ % (nr_cols - 1, data_path))
    elif plot_type == 'clustered_boxes':
        cmds.append("""
        plot "%s" using 2:xtic(1) title column, for [i=3:%s] '' \
                using i title column;
        """ % (data_path, nr_cols))

    return '\n'.join(cmds)

def plot(data, plot_type, output, xtitle, ytitle, xlog, ylog, xtics_rotate,
        font, size):
    tmp_path = tempfile.mkstemp()[1]
    with open(tmp_path, 'w') as f:
        f.write(data)

    nr_cols = len(data.split('\n')[0].split())
    nr_recs = len(data.split('\n\n')) - 1

    gnuplot_cmd = gen_gp_cmd(tmp_path, nr_recs, nr_cols, plot_type, output,
            xtitle, ytitle, xlog, ylog, xtics_rotate, font, size)

    subprocess.call(['gnuplot', '-e', gnuplot_cmd])
    os.remove(tmp_path)

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

    plot(data, plot_type, output, args.xtitle, args.ytitle,
            args.xlog, args.ylog, args.xtics_rotate, args.font, args.size)

if __name__ == '__main__':
    main()
