#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import tempfile

import plot_stdout
import transform_data_format

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('out', metavar='<file>', help='output file',
            default='plot.pdf', nargs='?')
    parser.add_argument('--file', '-f', metavar='<file>', help='data file')
    parser.add_argument('--data_fmt', choices=['recs', 'table'],
            help='format of the data')
    parser.add_argument('--xtime_fmt', metavar='<date format>',
            help='set xdata as time of the format')
    parser.add_argument('--type', '-t',
            choices=['scatter', 'scatter-yerr', 'labeled-lines',
                'clustered_boxes', 'clustered_boxes-yerr', 'heatmap'],
            default='scatter', help='plot type')
    parser.add_argument('--pointsize', metavar='<size>', help='size of point')
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

    parser.add_argument('--stdout_cols', type=int, default=80,
            help='max number of columns for stdout plot')
    parser.add_argument('--stdout_val_type', choices=['bytes', 'seconds'],
            help='type of the value')
    parser.add_argument('--stdout_first_row_display',
            help='string to display at first row')
    parser.add_argument('--stdout_first_col_display', nargs='+',
            help='string to display at first column')
    parser.add_argument('--stdout_heatmap_colorset',
            choices=['grayscale', 'green'], default='grayscale',
            help='heatmap color set')
    return parser.parse_args()

def gen_gp_cmd(data_path, nr_recs, nr_cols, args):
    xtime_fmt = args.xtime_fmt
    plot_type = args.type
    pointsize = args.pointsize
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

    if xtime_fmt:
        cmds += ['set xdata time;']
        cmds += ['set timefmt "%s";' % xtime_fmt]

    if pointsize:
        cmds += ['set pointsize %s;' % pointsize]

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
                nr_recs - 1, data_path)
        cmd += 'title columnheader(1);'
    elif plot_type == 'scatter':
        cmd = 'plot for [i=0:%s] "%s" index i using 1:2 with linespoints ' % (
                nr_recs - 1, data_path)
        cmd += 'title columnheader(1);'
    elif plot_type == 'labeled-lines':
        cmd = 'plot for [i=0:%s] "%s" ' % (nr_recs - 1, data_path)
        cmd += 'index i using 2:xtic(1) with linespoints '
        cmd += 'title columnheader(1);'
    elif plot_type == 'clustered_boxes-yerr':
        nr_realcols = (nr_cols - 1) / 2
        cmd = 'plot for [i=2:%d:2] "%s" using i:i+1:xtic(1) title col(i);' % (
                nr_cols - 1, data_path)
    elif plot_type == 'clustered_boxes':
        cmd = 'plot "%s" using 2:xtic(1) title column, for [i=3:%s] ""' % (
                data_path, nr_cols)
        cmd += 'using i title column;'
    elif plot_type == 'heatmap':
        cmd = 'plot "%s" using 1:2:3 with image title ""' % (data_path)
    cmds.append(cmd)

    return '\n'.join(cmds)

def plot(data, args):
    show_gpcmds = args.gnuplot_cmds
    data_fmt = args.data_fmt
    plot_type = args.type

    if data_fmt == 'recs' and plot_type == 'clustered_boxes':
        data = transform_data_format.recs_to_tbl(data)
        data_fmt = 'table'
    elif data_fmt == 'table' and plot_type in ['scatter', 'labeled-lines']:
        data = transform_data_format.tbl_to_recs(data)
        data_fmt = 'recs'
    elif data_fmt == 'table' and plot_type == 'scatter-yerr':
        data = tbl_to_yerr_recs(data)
        data_fmt = 'recs'

    if data_fmt == 'recs' and plot_type in ['clustered_boxes-yerr',
            'heatmap']:
        print('data format should be table for %s plot type' % plot_type)
        exit(1)
    elif data_fmt == 'table' and plot_type == 'scatter-yerr':
        print('data format should be recs for %s plot type' % plot_type)
        exit(1)

    tmp_path = tempfile.mkstemp(prefix='lbx-', suffix='.data')[1]
    with open(tmp_path, 'w') as f:
        f.write(data)

    nr_cols = len(data.split('\n')[0].split())
    nr_recs = len(data.split('\n\n'))

    gnuplot_cmd = gen_gp_cmd(tmp_path, nr_recs, nr_cols, args)
    if show_gpcmds:
        print(gnuplot_cmd)

    subprocess.call(['gnuplot', '-e', gnuplot_cmd])
    os.remove(tmp_path)

def main():
    args = get_args()

    output = args.out

    f = sys.stdin
    if args.file:
        f = open(args.file, 'r')
    data = f.read()
    f.close()

    if output == 'stdout':
        return plot_stdout.plot(data, args)

    out_extension = output.split('.')[-1]
    if not out_extension in ['pdf', 'jpeg', 'png', 'svg']:
        print("Unuspported output type '%s'." % out_extension)
        exit(-1)

    plot(data, args)

if __name__ == '__main__':
    main()
