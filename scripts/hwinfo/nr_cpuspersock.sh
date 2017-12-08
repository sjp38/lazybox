#!/bin/bash

grep "^core id" /proc/cpuinfo | sort | uniq | wc -l
