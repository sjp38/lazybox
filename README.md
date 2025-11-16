Lazybox
=======

`lazybox` is a toolbox for helping lazy hackers.

History of Lazybox and ongoing reorganization
=============================================

The project has started as a collection of scripts that helps automation of
performance evaluation experiments.  More specifically, for automating runs and
terminations of worklaods in parallel, e.g., running a workload with profiler
with variable a/b/c.  `run_exps.py` was the main body.

Some scripts for misc works have started being added into scripts/ directory.
As time goes by, more and more tools have added.  Some tools are even placed
under the root, instead of the `scripts/` directory.  As a result, `lazybox`
became just a collection of random tools.  But the original tools
(`run_exps.py` and its friends) for the specific purpose are still placed at
the root, and REAME was wrongly describing this project.  Some tools under
`scripts/` has also became large enough to deserve a directory under the root.

To make things easier to find and manage, we started reorganization from
2024-03-02.  Because some projects are apparently depending on lazybox, we will
try to make non-destructive ways.  We will keep old files and copy those to new
location, notify the alternatives, wait until existing users update to use the
new location, and finally destroy old things.

As of 2025-11-16, the original part of this project (`run_exps.py` and its
frieds) is moved to `parallel_runs`.  All users should update their setups to
use the tools under the new directory.

Version Compatibility
=====================

Lazybox v1.0 has released by 2020-01-01.  Lazybox later than the version will
not be strictly compatible with the v1.0.  Therefore, if you have scripts
depends on Lazybox v1.0 or earlier versions, please use the older version or
test it again with newer version.
