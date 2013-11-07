# Introduction
Help performance evaluation experiments automation.

# Usage
`$ run_exps.py <experiments specification file>`

## Experiments Specification File
Text file which specifies what experiments should be done.
Consists with zero or more experiments. Each experiments seperated by one or
more blank line.

Each experiment consists with zero or more commands which should be done as
part of experiment. Each command have specific type.

It would be better to make your own script or program which help to write your
own *experiments specification file* rather than write whole experiments you
want manually using hand.

### Type of command
 * start: Commands which should be done before experiment start.
   e.g., kernel module loading or program build
 * main: Main workload. Experiments will be end after command(s) of this type
   end.
 * back: Background command which should be run while main type commands run.
   e.g., profiling
 * end: Commands which should be done after experiment end.
   e.g., kernel modul unloading or meta files cleanup

### Example
Below is an example for *experiments specification file*
```
start: git checkout v1.0
start: make -j
start: insmod sjp.ko
main: ./workload/workload1
main: ./workload/workloadtogether
back: perf record -o perfout.data -a
back: vmstat 2 > vmstatout.data
end: rmmod sjp
end: make clean

start: git checkout v1.1
start: make -j
start: insmod sjp.ko
main: ./workload/workloadalone
back: perf record -o perfout.data -a
back: vmstat 2 > vmstatout.data
end: rmmod sjp
end: make clean
end: git checkout master
```

# License
GPL v3

# Author
SeongJae Park (sj38.park@gmail.com)
