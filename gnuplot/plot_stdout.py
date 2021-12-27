#!/usr/bin/env python3

import collections

import transform_data_format

def bytes_to_txt(val):
    if val < 1<<10:
        return '%d B' % val
    if val < 1<<20:
        return '%.3f KiB' % (val / (1<<10))
    if val < 1<<30:
        return '%.3f MiB' % (val / (1<<20))
    if val < 1<<40:
        return '%.3f GiB' % (val / (1<<30))
    return '%.3f PiB' % (val / (1<<40))

def seconds_to_txt(val):
    minute = 60
    hour = minute * 60
    day = hour * 24

    txt = ''
    days = val // day
    if days:
        txt = '%dd' % days
        val -= days * day

    hours = val // hour
    if hours:
        txt += '%dh' % hours
        val -= hours * hour

    mins = val // minute
    if mins:
        txt += '%dm' % mins
        val -= mins * minute

    txt+='%ds' % val
    return txt

def format_val_txt(val, val_type):
    'Transform value to human-readable text'
    if val_type == 'bytes':
        return bytes_to_txt(val)
    elif val_type == 'seconds':
        return seconds_to_txt(val)
    return '%s' % val

def colored_text(bgcolor, fgcolor, text):
    return u'\u001b[48;5;%dm\u001b[38;5;%dm%s' % (bgcolor, fgcolor, text)

def print_colored_text(colored_text):
    print(colored_text + u'\u001b[0m')

def plot_heatmap(data, args):
    colorsets = {
            'grayscale': {
                'bg': [237, 239, 241, 243, 245, 247, 249, 251, 253, 255],
                'fg': [232] * 10},
            'green': {
                'bg': [22, 58, 64, 65, 70, 71, 76, 77, 10, 11],
                'fg': [232] *10},
            }
    rows = []
    row = []
    for line in data.strip().split('\n'):
        if line.startswith('#'):
            continue
        x, y, z = [int(x) for x in line.split()]
        if len(row) > 0 and row[-1][0] != x:
            rows.append(row)
            row = []
        row.append([x, y, z])
    rows.append(row)

    min_z = None
    max_z = None
    for row in rows:
        for point in row:
            if min_z == None or point[2] < min_z:
                min_z = point[2]
            if max_z == None or point[2] > max_z:
                max_z = point[2]

    unit = (max_z - min_z) / 9
    colorset = colorsets[args.stdout_heatmap_colorset]
    bgcolors = colorset['bg']
    fgcolors = colorset['fg']
    if args.stdout_first_row_display:
        print(args.stdout_first_row_display)
    for idx, row in enumerate(rows):
        to_print = []
        if args.stdout_first_col_display:
            to_print.append(args.stdout_first_col_display[idx])
        for point in row:
            heat = int((point[2] - min_z) / unit)
            bgcolor = bgcolors[heat]
            fgcolor = fgcolors[heat]
            to_print.append(colored_text(bgcolor, fgcolor, heat))
        print_colored_text(''.join(to_print))
    print('# color samples: ', end='')
    print_colored_text(''.join([colored_text(bgcolors[x], fgcolors[x], x)
        for x in range(10)]))
    print('# values range: [%d-%d]' % (min_z, max_z))
    print('# unit of the number: %.3f' % unit)

def plot(data, args):
    if args.data_fmt == 'table':
        data = transform_data_format.tbl_to_recs(data)

    if args.type == 'heatmap':
        return plot_heatmap(data, args)

    title = None
    min_y = None
    max_y = None
    max_x_len = 0
    max_y_len = 0
    records = collections.OrderedDict()
    for line in data.strip().split('\n'):
        line = line.strip()
        if line.startswith('#'):
            continue
        fields = line.split()
        if len(fields) == 1:
            title = fields[0]
            records[title] = []
            continue
        if len(fields) < 2:
            continue

        try:
            x = fields[0]
            y = int(fields[1])
        except ValueError:
            continue

        x_len = len(x)
        if x_len > max_x_len:
            max_x_len = x_len
        y_len = len(format_val_txt(y, args.stdout_val_type))
        if y_len > max_y_len:
            max_y_len = y_len

        if not min_y or min_y > y:
            min_y = y
        if not max_y or max_y < y:
            max_y = y

        records[title].append([x, y])

    # one space between x and y, one space between y and bar, and '|' at start
    # and end of the bar
    max_len_bar = args.stdout_cols - max_x_len - max_y_len - 2 - 2
    sz_col = (max_y - min_y) / max_len_bar

    for title, values in records.items():
        print(title)
        for pair in values:
            x = pair[0]
            y = pair[1]

            x_str = '%s' % x
            x_str += ' ' * (max_x_len - len(x_str))
            y_str = format_val_txt(y, args.stdout_val_type)
            y_str += ' ' * (max_y_len - len(y_str))

            len_bar = int((y - min_y) / sz_col)
            len_spaces = max_len_bar - len_bar
            bar = '|%s%s|' % ('*' * len_bar, ' ' * len_spaces)
            print('%s %s %s' % (x_str, y_str, bar))
        print()

    print('# %s-%s in max %d columns bar (%.3f per column)' %
            (format_val_txt(min_y, args.stdout_val_type),
                format_val_txt(max_y, args.stdout_val_type),
                max_len_bar, sz_col))
