#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import tempfile

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('out', metavar='<file>', help='output file')
    parser.add_argument('--file', '-f', metavar='<file>', help='data file')
    parser.add_argument('--type', '-t',
            choices=['scatter', 'scatter-yerr',
                'clustered_boxes', 'clustered_boxes-yerr'],
            default='scatter', help='plot type')
    parser.add_argument('--font', metavar='<font>', help='font and size')
    parser.add_argument('--size', metavar='<width,height>',
            help='size of plotted image')
    parser.add_argument('--title', metavar='<title>', help='title of plot')
    parser.add_argument('--xtitle', '-x', metavar='<title>',
            help='x axis title')
    parser.add_argument('--ytitle', '-y', metavar='<title>',
            help='y axis title')
    parser.add_argument('--xrange', metavar='<range>', help='x-axis range')
    parser.add_argument('--yrange', metavar='<range>', help='y-axis range')
    parser.add_argument('--xlog', action='store_true',
            help='plot x axis in logscale')
    parser.add_argument('--ylog', action='store_true',
            help='plot y axis in logscale')
    parser.add_argument('--xtics_rotate', metavar='<degree>', type=int,
            help='xtics rotate degree')
    parser.add_argument('--gnuplot_cmds', action='store_true',
            help='print gnuplot commands')
    return parser.parse_args()

def gen_gp_cmd(data_path, nr_recs, nr_cols, args):
    plot_type = args.type
    output = args.out
    title = args.title
    xtitle = args.xtitle
    ytitle = args.ytitle
    xrange_ = args.xrange
    yrange = args.yrange
    xlog = args.xlog
    ylog = args.ylog
    xtics_rotate = args.xtics_rotate
    font = args.font
    size = args.size

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

    if title:
        cmds += ['set title "%s";' % title]
    if xtitle:
        cmds += ['set xlabel "%s";' % xtitle]
    if ytitle:
        cmds += ['set ylabel "%s";' % ytitle]

    if xrange_:
        cmds += ['set xrange %s;' % xrange_]
    if yrange:
        cmds += ['set yrange %s;' % yrange]

    log = ''
    if xlog:
        log += 'x'
    if ylog:
        log += 'y'
    if log:
        cmds += ['set logscale %s;' % log]

    if plot_type == 'scatter-yerr':
        cmd = 'plot "%s" using 1:2:3 linestyle 1 with yerrorbars notitle, ' % (
                data_path)
        cmd += 'for [i=0:%s] "%s" index i using 1:2 with linespoints ' % (
                nr_recs, data_path)
        cmd += 'title columnheader(1);'
    elif plot_type == 'scatter':
        cmd = 'plot for [i=0:%s] "%s" index i using 1:2 with linespoints ' % (
                nr_recs, data_path)
        cmd += 'title columnheader(1);'
    elif plot_type == 'clustered_boxes-yerr':
        nr_realcols = (nr_cols - 1) / 2
        cmd = 'plot for [i=2:%d:2] "%s" using i:i+1:xtic(1) title col(i);' % (
                nr_cols - 1, data_path)
    elif plot_type == 'clustered_boxes':
        cmd = 'plot "%s" using 2:xtic(1) title column, for [i=3:%s] ""' % (
                data_path, nr_cols)
        cmd += 'using i title column;'
    cmds.append(cmd)

    return '\n'.join(cmds)

def plot(data, args):
    show_gpcmds = args.gnuplot_cmds

    tmp_path = tempfile.mkstemp()[1]
    with open(tmp_path, 'w') as f:
        f.write(data)

    nr_cols = len(data.split('\n')[0].split())
    nr_recs = len(data.split('\n\n')) - 1

    gnuplot_cmd = gen_gp_cmd(tmp_path, nr_recs, nr_cols, args)
    if show_gpcmds:
        print(gnuplot_cmd)

    subprocess.call(['gnuplot', '-e', gnuplot_cmd])
    os.remove(tmp_path)

def main():
    args = get_args()

    output = args.out
    out_extension = output.split('.')[-1]
    if not out_extension in ['pdf', 'jpeg', 'png', 'svg']:
        print("Unuspported output type '%s'." % out_extension)
        exit(-1)

    f = sys.stdin
    if args.file:
        f = open(args.file, 'r')
    data = f.read()
    f.close()

    plot(data, args)

if __name__ == '__main__':
    main()
