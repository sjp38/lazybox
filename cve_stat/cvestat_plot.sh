#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <cve dump json file>"
	exit 1
fi

cve_json=$1

bindir=$(dirname "$0")

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric broken_to_reported | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE is committed to be reported" \
	--size 1024,768 \
	--font "TimesNewRoman" "broken_to_reported_linear.png"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric broken_to_reported --min_val 1 | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE is committed to be reported" \
	--size 1024,768 \
	--font "TimesNewRoman" --ylog "broken_to_reported.png"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_authored | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be authored" \
	--size 1024,768 \
	--font "TimesNewRoman" "report_to_fix_authored_linear.png"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_committed | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be committed" \
	--size 1024,768 \
	--font "TimesNewRoman" "report_to_fix_committed_linear.png"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_authored --min_val 1 | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be authored" \
	--size 1024,768 \
	--font "TimesNewRoman" --ylog "report_to_fix_authored.png"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_committed --min_val 1 | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be committed" \
	--size 1024,768 \
	--font "TimesNewRoman" --ylog "report_to_fix_committed.png"
