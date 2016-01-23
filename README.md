Lazybox
=======

`lazybox` is a collection of scripts that helps automation of performance
evaluation experiments. However, it can be used for automation of general
computer program execution.


Abstract
========

Performance evaluation experiments are hard to be done manually by people. It's
basically repetitive and time consuming. To be practical, most people automate
the experiments. Because each experiments have particular characterizations and
limitations, However, most automation code could not be reused easily.

This project aims to

1. generalize those experiments and
2. develop reusable, useful tools and structure for automation.


Introduction
============

This project is composed with two main programs. Each program is for automation
of local experiments and remote experiments.

For automation of basic experiments that consists of multiple small experiments
in local system(e.g., measure execution time of program a and program b when
they run in same system), lazybox provides `run_exps.py` program.
User can describes what experiments they want and how those small experiments
should be executed for their evaluation using text configuration file.
The program `run_exps.py` executes those experiments described in
the configuration file on local machine.
For detail, refer to Section `Local Experiments Automation` below.

Lots of experiments are done not only inside a local machine, but also within
server - client environment, cluster or network of machines.
Event though the workload user trying to do experiments can be done within
single machine, it can be convenient to do the experiments from remote host if
the experiments contains reboot workload.
To support those case, we provide a `expect` script, `remote_exps.exp` script.
It connects to remote target machine via ssh and spawn `run_exps.py` from
there.
For that, `lazybox` should be installed on target machine at first. For detail,
refer to Section `Remote experiments` below.


Local Experiments Automation
============================

`$ run_exps.py <experiments specification file>`


Experiments Specification File
------------------------------

Experiments specification file is a text file which specifies what experiments
should be done how.
A experiment can be configured with multiple small experiments. For example,
measuring execution time of program a while program b is running on same
machine in background.
Multiple big experiments can be described in one experiments specification
file.
Each big experiment is seperated by one or more blank line(s).

Experiment consists with zero or more bash commands(small experiment) which
should be done as part of experiment.
Each command have specific type which specifies when and how the command should
be executed.

If your experiments are too big and repetitive, consider to write your own
experiments specification file generator rather than write it down manually in
miserable way. For detail, see below section, [Experiments Specification File
Generator](#Experiments Specification File Generator).

### Type of commands
 * `start`: Commands which should be done before experiment start.
   (e.g., kernel module loading or program build)
   If multiple start command is described, those commands will be executed
   sequentially.
 * `main`: Main workload. Experiments will be end after command(s) of this type
   end. If multiple main workloads exist, they will be executed concurrently
   and workloads terminated earlier will be executed repeatedly until slowest
   workload be terminated.
 * `back`: Background command which should be run while main type commands run.
   Unlike main commands, if back workload is terminated earlier than main
   workload(s), it does not repeat execution automatically. If you want back
   workload to run infinitely until main workload run, it should be described as
   main command or use `bash` loop inside the command.
   (e.g., profiling or system stressing task)
 * `end`: Commands which should be done after experiment end.
   (e.g., kernel modul unloading or meta files cleanup)
   If multiple end command is described, those commands will be executed
   sequentially as start commands do.
 * `check`: Check whether experiment was successful. Commands be executed after
   end commands end and notifies check result using return code. Return code 0
   means sucess, other values means failure. If any one of check command says
   failed, the experiment be executed again until success up to 10 times.

### Example
Below is an example for *experiments specification file*
```
start git checkout v1.0
start make -j
start insmod sjp.ko
main ./workload/workload1 > work1.out
main ./workload/workloadtogether > work2.out
back perf record -o perfout.data -a
back vmstat 2 > vmstatout.data
end rmmod sjp
end make clean
check grep success work1.out
check grep success work2.out

start git checkout v1.1
start make -j
start insmod sjp.ko
main ./workload/workloadalone
back perf record -o perfout.data -a
back vmstat 2 > vmstatout.data
end rmmod sjp
end make clean
end git checkout master
```

Experiments Specification File Generator
----------------------------------------

For simplicity, we do not support describing experiment in procedural way.
Using `loop` or `goto` inside specification file would be complex to be read.
In other word, experiments should be described in linearly executable way.

However, constraining people to write down lots of repeating experiments
manually is crime against humanity.
For the reason, we recommend to develop and use their own experiments
specification file generator.
To help the process, we provide simple stub generator, `generate_exp_conf.py`.
It contains essential code for automated experiments specification file
generator.

### Usage of the stub
1. Copy the stub
2. Edit main loop of experiments generation as you need
3. Run modified copy and redirect stdout to appropriate file
4. Use the file for `run_exps.py`


Remote Experiments Automation
=============================

For lots of case, experiments should be done within server - client
environment, cluster or network of machines.
Moreover, in some case, the experiments should be done on remote machine even
though the experiments itself can be done in single machine.
For example, suppose a case that each experiment should be done after reboot.

For the case, `lazybox` provides a `expect` script, `remote_exps.exp` script.
It log in to remote target machine via ssh and spawn `run_exps.py` from the
remote machine.
As you already expected, it means few precondition should be satisfied to use
`remote_exps.exp` script.
- The machine that executes `remote_exps.exp` script should already
  installed `expect`.
- `lazybox` should be installed and contains experiments specification file on
  the remote target machine.

Best manual is an example.
Refer `gcma_exps.py` for example.
It was used for real evaluation of a paper.
The evaluation contains lots of reboot of target machine and the script do
automation using `remote_exps.exp` inside.

Basic usage is as below:
```
$ expect remote_exps.exp \
              <username> <target> <ssh port> <password> \
              <lazybox path> <exp>
```


License
=======

GPL v3


Author
======

SeongJae Park (sj38.park@gmail.com)
