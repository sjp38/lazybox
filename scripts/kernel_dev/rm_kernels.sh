#!/bin/bash

pr_usage()
{
	echo "Usage: $0 [OPTION]... [target kernel version]..."
	echo
	echo "OPTION"
	echo "  --except_old <number>	Leave <number> oldest kernels"
	echo "  --except_new <number>	Leave <number> latest kernels"
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

kernels_to_remove=()
except_old_nr=0
except_new_nr=0

while [ $# -ne 0 ]
do
	case $1 in
	"--except_old")
		if [ $# -lt 2 ]
		then
			echo "<number> not given"
			pr_usage_exit 1
		fi
		except_old_nr=$2
		shift 2
		continue
		;;
	"--except_new")
		if [ $# -lt 2 ]
		then
			echo "<number> not given"
			pr_usage_exit 1
		fi
		except_new_nr=$2
		shift 2
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
		break
		;;
	esac
done

bindir=$(dirname "$0")
read -r -a kernels <<< "$("$bindir/ls_kernels.py")"

rm_start=$except_old_nr
rm_end=$((${#kernels[@]} - except_new_nr))

for ((i = 0 ; i < ${#kernels[@]} ; i++))
do
	echo "$i"
	if [ $i -lt $rm_start ] || [ $i -ge $rm_end ]
	then
		continue
	fi
	kernels_to_remove+=("${kernels[$i]}")
done

if [ "$EUID" -ne 0 ]
then
	echo "run as root, please"
	exit 1
fi

for ver in "${kernels_to_remove[@]}"
do
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
update-grub2
