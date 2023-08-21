TL; DR
------

About 95% of CVEs that affect the mainline tree has fixed before those are
reported by `linux_kernel_cves` project.  The number was 76%, 69%, 73%, 78%,
83% and 82% for 6.4.y, 6.1.y, 5.15.y, 5.10.y, 5.4.y, 4.19.y, and 4.14.y,
respectively.

The worst case time between linux_kernel_cves report and fix commit being fixed
was [16, 32) weeks for the mainline.  For the stable trees, the number was
[4, 8) weeks (6.4.y), [16, 32) weeks (6.1.y and 5.15.y), [32, 64) weeks
(5.10.y), [64, 128) weeks for 5.4.y, [32, 64) weeks (4.19.y and 4.14.y).

Motivation: Airplane Delay
--------------------------

It is well known that CVEs are only making kernel hackers frustrated[1].
Rcently, from a discussion on maintainers summit topic, Greg mentioned[2] 99%
of CVEs are reported after those are already fixed on LTS kernels.  He also
mentions the data is produced by Google security team, for 2 years straight.

There is no doubt about the overall arguments, but I got curious if I will be
able to get the data from Google security team, and if I could further generate
that on my own.  Yesterday, I heard my airplane is delayed for more than two
hours, and I realized that this could be a fun small hack to do to forget about
it.  So I wrote a little and buggy scripts set[3] and ran it.  Summarizing the
results here.

Disclaimer
----------

To reproduce the data, knowing when each CVE has first reported is needed.
However, I don't know well about CVE and I don't want to dare to access to some
serious CVE project databases.  Therefore, I decicded to use linux_kernel_cves
project[4].  I retrieve basic CVE information such as which CVEs are affecting
which trees, which commits have introduced the CVE, and which commits fix which
CVEs, from there, and use `git blame` output on it as the source of a data that
resembles the first report dates of CVEs.  Since the project is usually updated
later than other government site-like place, this would added not modest level
of errors.  Of course, the scripts may have many uninteded bugs.

Data Sources
------------

As mentioned above, I use linux_kernel_cves as the important source of data.
Specifically, I use b3862f27d9f2 ("Update 10Aug23") commit of the repo for this
summary.

The initial commit of linux_kernel_cves have authroed at 2017-02-08.  I hence
didn't use CVEs that having <2019 report-year-part in their CVE id (e.g.,
CVE-2018-XXXX) for makin this summary.

How many CVEs are fixed before be reported?
-------------------------------------------

About 95% of CVEs that affecting the mainline tree (Linus Torvalds' master
branch) has fixed (committed) before be reported by linux_kernel_cves.  About
89% of those were fixed even more than 1 weeks before the report.  So, though
this hack should have many errors, this results seems align with Greg's claim.
About 31% of those were even fixed more than 64 weeks before the report.

The number drops a little bit for LTS kernels, though.  6.1.y, 5.15.y, 5.10.y,
and 5.4.y LTS trees fixed about 76%, 69%, 73%, and 78% of CVEs before reported
by linux_kernel_cves, respectively.  Interestingly, the numbers increase again
with older LTSes.  4.19.y and 4.14.y LTS kernels fixed about 83% and 82% of
CVEs before reported by linux_kernel_cves, respectively.

I just assume that could be because CVE reporters also evolved from some point
between 4.14.y and 5.4.y, but that's just my personal and humble theory off the
top of my head.

How long after the report CVEs be fixed?
----------------------------------------

About 3.635% of CVEs that affecting the mainline has fixed (committed) after
linux_kernel_cves reported those.  Remaining 1.268% CVEs are still not having
fixes.  In the worst case, a CVE has fixed in [16, 32) weeks after the
linux_kernel_cves report.

The worst-case fix time tended to increase for old kernels.  It was [4, 8)
weeks for 6.4.y, [16, 32) wekks for both 6.1.y and 5.15.y LTS trees, [32, 64)
weeks for 5.10.y, [64, 128) weeks for 5.4.y, [32, 64) weeks for 4.19.y, and
[32, 64) weeks for 4.14.y.

More Visualization
------------------

I visualized some more statistics including the distribution of

- the time between the commit of the CVE-introducing buggy commit and the
  linux_kernel_cves report of the CVE[5],
- above data for more than one day in logscale[6],
- the time between the linux_kernel_cves report and the fix commit being
  authored[7],
- above data for more than one day in logscale[8],
- the time between the linux_kernel_cves report and the fix commit being
  committed[9], and
- above data for more than one day in logscale[10]

using a script[11].

Conclusion
----------

Playing with this kind of data is fun itself, and sharing the results and the
source code is beneficial for not only me.  I wrote most of this scripts while
waiting airplane, so it may contain many bugs, and my review of the results may
have biased opinions.  Please feel free to use it, and let me know if you find
such bugs or wrong interpretation of the results.  I now arrived to my
destination, but I might continue some more hacks on this, so asking of more
statistics and features is also welcome.

[1] https://kernel-recipes.org/en/2019/talks/cves-are-dead-long-live-the-cve/
[2] https://lore.kernel.org/ksummit/2023081540-vindicate-caterer-33c6@gregkh/
[3] https://github.com/sjp38/lazybox/tree/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat
[4] https://github.com/nluedtke/linux_kernel_cves
[5] https://github.com/sjp38/lazybox/blob/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat/report/broken_to_reported_linear.png
[6] https://github.com/sjp38/lazybox/blob/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat/report/broken_to_reported.png
[7] https://github.com/sjp38/lazybox/blob/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat/report/report_to_fix_authored_linear.png
[8] https://github.com/sjp38/lazybox/blob/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat/report/report_to_fix_authored.png
[9] https://github.com/sjp38/lazybox/blob/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat/report/report_to_fix_committed_linear.png
[10] https://github.com/sjp38/lazybox/blob/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat/report/report_to_fix_committed.png
[11] https://github.com/sjp38/lazybox/blob/bec4ed0259da655ea47e5478c8fe6f7850c1156b/cve_stat/plot.sh
