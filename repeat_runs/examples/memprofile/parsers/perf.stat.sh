#!/bin/bash

PFS=$1/perf.stat
grep "insns* per cycle" $PFS | awk '{print "ipc: " $4}' > $2/ipc
grep "page-faults" $PFS | awk '{print "page-faults: " $4}' > $2/pf
grep "LL-cache hits" $PFS | awk '{print "llcmiss: " $4}' | \
	sed -e 's/%//' > $2/llcmiss
