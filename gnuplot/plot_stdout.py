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

def plot(data, args):
    if args.data_fmt == 'table':
        data = transform_data_format.tbl_to_recs(data)

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
