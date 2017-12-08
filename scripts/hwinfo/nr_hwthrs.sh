#!/bin/bash

grep "^processor" /proc/cpuinfo | wc -l
