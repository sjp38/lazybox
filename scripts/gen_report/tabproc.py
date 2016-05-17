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

def atab_compose(tables, targets, labels):
    """Compose multiple tables into one tables.

    @tables     List of multiple tables to be composed.
    @targets    Target fields to be located inside composed table.
    @labels     Labels to be used to distinguish sub tables.

    Each table in tables should have same legend, same number of rows.  Each
    row in table should have same field for labels pointing field.
    """
    lable_idxs = keyindexs(tables[0].legend, labels)
    target_idxs = keyindexs(tables[0].legend, targets)

    new_legend = []
    for table in tables:
        label_vals = [table.rows[0][li] for li in lable_idxs]
        for target in targets:
            new_legend.append("%s-%s" %
                    ('_'.join([str(x) for x in label_vals]), target))

    ret = ATable("%s-%s" % ('_'.join(labels), '_'.join(targets)),
            new_legend, [])
    for idx, table in enumerate(tables):
        for ri, row in enumerate(table.rows):
            if idx == 0:
                ret.rows.append([])
            ret.rows[ri].extend([row[i] for i in target_idxs])
    return ret

def merge(tables):
    """Merge multiple tables into one tables."""
    new_legend = []
    for table in tables:
        for name in table.legend:
            new_legend.append("%s-%s" % (table.title, name))
    ret = ATable('_'.join([table.title for table in tables]), new_legend, [])

    for idx, table in enumerate(tables):
        for ridx, row in enumerate(table.rows):
            if idx == 0:
                ret.rows.append([])
            ret.rows[ridx].extend(row)
    return ret

def atab_split(tables, keys):
    """Split tables into multiple tables with same keys.

    Title of splitted tables will be the keys.
    """
    kidxs = keyindexs(tables.legend, keys)

    inter_map = {}
    for row in tables.rows:
        key = "%s" % [row[idx] for idx in kidxs]
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

    tables = atab_split(table, keys)
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
    splits = atab_split(t, ["system"])
    print atab_compose(splits, ["value1"], ["system"])
    print atab_compose(splits, ["value2"], ["system"])
    print atab_compose(splits, ["value1", "value2"], ["system"])
    print merge(splits)
