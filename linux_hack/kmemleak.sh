#!/bin/bash

kmemleak_file="/sys/kernel/debug/kmemleak"
echo scan > "$kmemleak_file"
cat "$kmemleak_file"
