#!/usr/bin/env python

"Module for tables processing for report"

import copy
import math

class ATable:
    title = None    # string
    legend = None   # list of strings
    rows = None     # list of lists of strings

    def __init__(self, title, legend, rows):
        self.title = title
        self.legend = legend
        self.rows = rows

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        str_ = "title: %s\n" % self.title
        str_ += "%s" % self.legend + "\n"
        for row in self.rows:
            str_ += "%s" % row + "\n"
        return str_

    def csv(self):
        lines = []
        lines.append("title,%s" % self.title)
        lines.append(",".join(str(x) for x in self.legend))
        for row in self.rows:
            lines.append(",".join(str(x) for x in row))
        return '\n'.join(lines)

def from_csv(csv):
    lines = csv.split('\n')
    title = lines[0].split(',')[1]
    legend = lines[1].split(',')
    rows = []
    for line in lines[2:]:
        rows.append([x for x in line.split(',')])
    return ATable(title, legend, rows)

def keyindexs(legend, keys):
    kidxs = []
    for k in keys:
        for idx, name in enumerate(legend):
            if k == name:
                kidxs.append(idx)
    return kidxs

def pick_fields(table, fields):
    """Reconstruct table with selected fields only"""
    fields_idxs = keyindexs(table.legend, fields)
    new_rows = []
    for row in table.rows:
        new_rows.append([row[idx] for idx in fields_idxs])
    return ATable(table.title, fields, new_rows)

def merge(tables):
    """Merge multiple tables into one tables.

    Tables should have same legend and same number of rows.
    """
    new_legend = []
    for table in tables:
        for name in table.legend:
            new_legend.append('-'.join([table.title, name]))
    ret = ATable('-'.join([table.title for table in tables]), new_legend, [])

    for idx, table in enumerate(tables):
        for ridx, row in enumerate(table.rows):
            if idx == 0:
                ret.rows.append([])
            ret.rows[ridx].extend(row)
    return ret

def split_with_key(tables, keys):
    """Split tables into multiple tables with same keys.

    Title of splitted tables will be the keys.
    """
    kidxs = keyindexs(tables.legend, keys)

    inter_map = {}
    for row in tables.rows:
        key = "%s" % '-'.join([str(row[idx]) for idx in kidxs])
        if not inter_map.has_key(key):
            inter_map[key] = ATable(key, tables.legend, [])
        inter_map[key].rows.append(row)
    return inter_map.values()

def __stat_of(vals):
    minv = min(vals)
    maxv = max(vals)
    avg = sum(vals) / len(vals)
    variance = float(sum([pow(v - avg, 2) for v in vals])) / len(vals)
    stdev_ = math.sqrt(variance)
    return [minv, maxv, avg, stdev_]

def stat_of(table, keys):
    """Get average, min/max values, standard deviation of values in a table
    with same keys.
    """
    new_legend = []
    for name in table.legend:
        new_legend.extend([name + "_min", name + "_max", name + "_avg",
                            name + "_stdev"])

    ret = ATable(table.title, new_legend, [])

    tables = split_with_key(table, keys)
    for subtable in tables:
        new_row = []
        ret.rows.append(new_row)
        for i in range(len(subtable.legend)):
            try:
                vals = [float(row[i]) for row in subtable.rows]
            except ValueError:
                val = subtable.rows[0][i]
                new_row.extend([val, val, val, val])
                continue
            new_row.extend(__stat_of(vals))
    return ret

def sort_with(tables, keys):
    kidxs = keyindexs(tables.legend, keys)
    for i in reversed(kidxs):
        tables.rows.sort(key=lambda x: x[i])
    return tables

if __name__ == "__main__":
    t = ATable("foo", ["key", "val", "something"],
            [
                [1, 1, 'a'], [1, 3, 'a'], [1, 5, 'a'],
                [2, 3, 'b'], [2,4,'b'], [2,5,'b'], [3, 5, 'c']])
    stat_calced = stat_of(t, ["key"])
    sorted = sort_with(stat_calced, ["key_avg"])
    print sorted
    print sorted.csv()
    print from_csv(sorted.csv())
    print sort_with(stat_of(from_csv(t.csv()), ["key"]), ["key_avg"])

    t = ATable("foo", ["thrs", "system", "value1", "value2"], [
                [1, 'A', 10, 90],
                [2, 'A', 20, 80],
                [4, 'A', 30, 70],
                [1, 'B', 40, 60],
                [2, 'B', 50, 50],
                [4, 'B', 60, 40],
                [1, 'sys', 70, 30],
                [2, 'sys', 80, 20],
                [4, "sys", 90, 10],
            ])
    splits = split_with_key(t, ["system"])
    print merge(splits)
    print pick_fields(merge(splits), ["A-thrs", "A-value1", "B-value1",
                                        "A-value2", "B-value2"])
