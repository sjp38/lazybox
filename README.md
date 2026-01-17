Lazybox
=======

`lazybox` is a toolbox for helping lazy hackers.

The tools are organized into subdirectories based on their purpose, as below.

- cve_stat: for making statistics about linux kernel cve.
- format_data: for visualizing raw data in human-redable texts and images.
- version_control: for various git and patches based SCM use cases including
  statistics, history tracking and patches queue management.
- humble_ci: for simple CI implementation.
- linux_hack: for various linux kernel hacking tasks including kernel
  build/install and kernel development stats.
- parallel_runs: for organizing parallel workloads/profilers runs.
- parallel_ssh_cmds: for managing parallel ssh commands to multiple remote
  machines.
- profile: for system/worklaods stat monitoring and profiling.
- repeat_runs: for running test/experiments for multiple times and
  organizing/analyzing the results.
- tune: for tuning and setting system operation knobs.
- unsorted: as the name says.
- workloads: for running test or stress workloads.

Stability
---------

The tools could be renamed frequently.  We aim to not break known users though.
Below are the known users.  If your project is using lazybox but your project
is not listed below, please request changes.

- [damon-hack](https://git.kernel.org/pub/scm/linux/kernel/git/sj/damon-hack.git/)
- [damon-tests](https://github.com/damonitor/damon-tests)
