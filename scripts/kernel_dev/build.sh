#!/bin/bash

set -e

pr_usage()
{
	echo "
Usage: $0 [OTION]... <src dir> <build dir>

OPTION
  --config	Config file to append
  --install	Install built kernel
  --reboot	Reboot after install
"
}

pr_msg_usage_exit()
{
	msg=$1
	exit_code=$2
	echo "$msg"
	pr_usage
	exit "$exit_code"
}

src_dir=""
build_dir=""
additional_config=""
do_install="false"
do_reboot="false"
while [ $# -ne 0 ]
do
	case $1 in
	"--config")
		if [ $# -lt 2 ]
		then
			pr_msg_usage_exit "--config argument is not given" 1
		fi
		additional_config=$2
		shift 2
		continue
		;;
	"--install")
		do_install="true"
		shift 1
		continue
		;;
	"--reboot")
		do_reboot="true"
		shift 1
		continue
		;;
	*)
		if [ $# -lt 2 ]
		then
			pr_msg_usage_exit "src and build dirs not given" 1
		fi
		if [ ! "$src_dir" = "" ]
		then
			pr_msg_usage_exit "more than one src dir given" 1
		fi
		src_dir=$1
		build_dir=$(realpath $2)
		shift 2
		;;
	esac
done

bindir=$(dirname "$0")

if [ "$src_dir" = "" ]
then
	pr_msg_usage_exit "src dir not given" 1
fi

orig_config=$build_dir/.config

if [ ! -d "$build_dir" ]
then
	mkdir "$build_dir"
fi

if [ ! -f "$orig_config" ]
then
	cp "/boot/config-$(uname -r)" "$orig_config"
fi

if [ ! "$additional_config" = "" ]
then
	cat "$additional_config" >> "$build_dir/.config"
fi

make -C "$src_dir" O="$build_dir" olddefconfig
make -C "$src_dir" O="$build_dir" -j$(nproc)

if [ "$do_install" = "true" ]
then
	sudo make -C "$src_dir" O="$build_dir" modules_install install
	kernelversion=$(make -C "$src_dir" O="$build_dir" -s kernelrelease)
	sudo "$bindir/set_kernel.py" "$kernelversion"
fi

if [ "$do_reboot" = "true" ]
then
	echo "reboot now"
	sudo shutdown -r now
fi
