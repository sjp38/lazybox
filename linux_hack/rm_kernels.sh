#!/bin/bash

pr_usage()
{
	echo "Usage: $0 [OPTION]... [target kernel version]..."
	echo
	echo "OPTION"
	echo "  --except <old> <new>	Leave <old> old and <new> new kernels"
	echo "  --except_new <number>	Leave <number> latest kernels"
	echo "  --dry			Make no change but notify what will do"
	echo "  -h, --help		Show this message"
}

pr_usage_exit()
{
	exit_code=$1

	pr_usage
	exit "$exit_code"
}

if [ $# -lt 1 ];
then
	pr_usage_exit 1
fi

bindir=$(dirname "$0")
# newest kernel comes first
kernels=($("$bindir/ls_kernels.py"))

kernels_to_remove=()
except_old_nr=${#kernels[@]}
except_new_nr=${#kernels[@]}
dry_run="false"
target_specified="false"

while [ $# -ne 0 ]
do
	case $1 in
	"--except")
		if [ $# -lt 3 ]
		then
			echo "<number> not given"
			pr_usage_exit 1
		fi
		except_old_nr=$2
		except_new_nr=$3
		target_specified="true"
		shift 3
		continue
		;;
	"--dry")
		dry_run="true"
		shift 1
		continue
		;;
	"--help" | "-h")
		pr_usage_exit 0
		;;
	*)
		if [ "$except_old_nr" = "" ] && [ "$except_new_nr" = "" ] &&
			[ $# -lt 1 ]
		then
			echo "<target kernel version> not given"
			pr_usage_exit 1
		fi
		kernels_to_remove=($@)
		target_specified="true"
		break
		;;
	esac
done

if [ ! "$target_specified" = "true" ]
then
	echo "Target kernels to remove are not specified"
	pr_usage_exit 1
fi

current_kernel=$(uname -r)
rm_start=$except_new_nr
rm_end=$((${#kernels[@]} - except_old_nr))

for ((i = 0 ; i < ${#kernels[@]} ; i++))
do
	if [ $i -lt $rm_start ] || [ $i -ge $rm_end ]
	then
		continue
	fi
	if [ "${kernels[$i]}" = "$current_kernel" ]
	then
		continue
	fi
	kernels_to_remove+=("${kernels[$i]}")
done

for ((i = 0 ; i < ${#kernels_to_remove[@]} ; i++))
do
	if [ "${kernels_to_remove[$i]}" = "$current_kernel" ]
	then
		unset 'kernels_to_remove[i]'
	fi
done

if [ "$EUID" -ne 0 ] && [ "$dry_run" = "false" ]
then
	echo "run as root, please"
	exit 1
fi

for ver in "${kernels_to_remove[@]}"
do
	if [ "$dry_run" = "true" ]
	then
		echo "Remove $ver"
		continue
	fi
	if [ ! -e "/boot/vmlinuz-$ver" ]
	then
		echo "vmlinuz-$ver not found"
		continue
	fi

	rm "/boot/vmlinuz-$ver"
	rm "/boot/initrd.img-$ver"
	rm "/boot/System.map-$ver"
	rm "/boot/config-$ver"
	rm -fr "/lib/modules/$ver"
	rm "/var/lib/initramfs-tools/$ver"
done
if [ "$dry_run" = "true" ]
then
	exit 0
fi

update-grub2
