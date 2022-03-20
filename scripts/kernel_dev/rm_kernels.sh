#!/bin/bash

pr_usage()
{
	echo "Usage: $0 <target kernel version>..."
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

if [ "$EUID" -ne 0 ]
then
	echo "run as root, please"
	exit 1
fi

for ver in "${@:1}"
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
