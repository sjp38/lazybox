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
	--font "TimesNewRoman, 5pt" "broken_to_reported_linear.pdf"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric broken_to_reported --min_val 1 | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE is committed to be reported" \
	--font "TimesNewRoman, 5pt" --ylog "broken_to_reported.pdf"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_authored | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be authored" \
	--font "TimesNewRoman, 5pt" "report_to_fix_authored_linear.pdf"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_committed | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be committed" \
	--font "TimesNewRoman, 5pt" "report_to_fix_committed_linear.pdf"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_authored --min_val 1 | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be authored" \
	--font "TimesNewRoman, 5pt" --ylog "report_to_fix_authored.pdf"

"$bindir/cvestat_percentile.py" "$cve_json" \
	--metric report_to_fix_committed --min_val 1 | \
	"$bindir/../gnuplot/plot.py" --data_fmt recs --type scatter \
	--pointsize 0.5 --xtitle "Percentile" \
	--ytitle "Days from a CVE be reported to the fix be committed" \
	--font "TimesNewRoman, 5pt" --ylog "report_to_fix_committed.pdf"
