#!/usr/bin/env python

"Module for numbers processing for report"

import math

class Numbers:
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

def group_by(numbers, keys):
    kidxs = []
    for k in keys:
        for idx, name in enumerate(numbers.legend):
            if k == name:
                kidxs.append(idx)

    inter_map = {}
    for row in numbers.rows:
        key = "%s" % [row[idx] for idx in kidxs]
        if not inter_map.has_key(key):
            inter_map[key] = []
        inter_map[key].append(row)
    return inter_map.values()

def stat_of(numbers, keys):
    """Get average, min/max values, standard deviation of numbers with same
    keys.
    """
    new_legend = []
    for name in numbers.legend:
        new_legend.extend([name + "_min", name + "_max", name + "_avg",
                            name + "_stdev"])

    ret = Numbers(numbers.title, new_legend, [])

    groups = group_by(numbers, keys)
    for group in groups:
        new_row = []
        ret.rows.append(new_row)
        for i in range(len(numbers.legend)):
            vals = [row[i] for row in group]
            minv = min(vals)
            maxv = max(vals)
            avg = sum(vals) / len(vals)
            variance = float(sum([pow(v - avg, 2) for v in vals])) / len(vals)
            stdev_ = math.sqrt(variance)
            new_row.extend([minv, maxv, avg, stdev_])
    return ret

def sort_with(numbers, keys):
    kidxs = []
    for k in keys:
        for idx, name in enumerate(numbers.legend):
            if k == name:
                kidxs.append(idx)
    for i in reversed(kidxs):
        numbers.rows.sort(key=lambda x: x[i])
    return numbers

if __name__ == "__main__":
    n = Numbers("foo", ["key", "val"], [[1, 1], [1, 3], [1, 5],
                                        [2, 3], [2,4], [2,5], [3, 5]])
    print sort_with(stat_of(n, ["key"]), ["key_avg"])
