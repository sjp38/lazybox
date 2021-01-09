#!/usr/bin/env python3

from collections import OrderedDict

def recs_to_tbl(data):
    recs = OrderedDict()

    paragraphs = data.split('\n\n')
    for p in paragraphs:
        label = None
        rec = OrderedDict()
        for line in p.split('\n'):
            if not line:
                continue
            if line.startswith('#'):
                continue
            if not label:
                label = line.strip()
                continue

            fields = line.split()
            if len(fields) != 2:
                print('record of fields != 2: %s' % line)
                exit(1)
            rec[fields[0]] = fields[1]

        recs[label] = rec

    rows = []
    rows.append('\t'.join(['xxx'] + list(recs.keys())))

    ref_rec_label = list(recs.keys())[0]
    for x in recs[ref_rec_label].keys():
        row = [x]
        for label in recs.keys():
            row.append(recs[label][x])
        rows.append('\t'.join(row))

    return '\n'.join(rows)

def tbl_to_recs(data):
    recs = OrderedDict()

    for line in data.split('\n'):
        if not line:
            continue
        if line.startswith('#'):
            continue
        fields = line.split()
        if len(recs) == 0:
            for f in fields[1:]:
                recs[f] = OrderedDict()
            continue
        labels = list(recs.keys())
        for idx, l in enumerate(labels):
            recs[l][fields[0]] = fields[idx + 1]

    rows = []
    for label in recs:
        rows.append(label)
        for x in recs[label]:
            rows.append('%s\t%s' % (x, recs[label][x]))
        rows.append('')
        rows.append('')
    return '\n'.join(rows).strip()

def tbl_to_yerr_recs(data):
    """
    Format is, for example:
        xxx     a   a_stdev b   b_stdev
        sysA    123 10      245 5
        sysB    15  1       40  3
    """
    recs = OrderedDict()

    for line in data.split('\n'):
        if not line:
            continue
        if line.startswith('#'):
            continue
        fields = line.split()
        if len(recs) == 0:
            for i in range(len(fields)):
                if i % 2 == 0:
                    continue
                recs[fields[i]] = OrderedDict()
            continue

        labels = list(recs.keys())
        for idx, l in enumerate(labels):
            recs[l][fields[0]] = [fields[idx * 2 + 1], fields[idx * 2 + 2]]

    rows = []
    for label in recs:
        rows.append(label)
        for x in recs[label]:
            rows.append('%s\t%s\t%s' %
                    (x, recs[label][x][0], recs[label][x][1]))
        rows.append('')
        rows.append('')
    return '\n'.join(rows).strip()
