#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 <number of old kernels to leave> \\"
	echo "		<number of new kernels to leave>"
	exit 1
fi

nr_old_kernels_to_leave=$1
nr_new_kernels_to_leave=$2

kernels=$("$bindir/ls_kernels.py")
nr_kernels=0
for kernel in $kernels
do
	nr_kernels=$((nr_kernels+1))
done

remove_start=$nr_old_kernels_to_leave
remove_end=$((nr_kernels - nr_new_kernels_to_leave))

kernels_to_remove=""
i=0
for kernel in $kernels
do
	i=$((i + 1))
	if [ $i -lt $remove_start ]
	then
		continue
	fi
	if [ $i -gt $remove_end ]
	then
		break
	fi
	kernels_to_remove+="$kernel "
done

echo "will remove $kernels_to_remove"

"$bindir/rm_kernels.sh" $kernels_to_remove
