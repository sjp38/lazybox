#!/bin/bash

if [ $# -lt 1 ];
then
	echo "Usage: $0 <target kernel version>..."
	exit 1
fi

if [ "$EUID" -ne 0 ]
then
	echo "run as root, please"
	exit 1
fi

for ver in "${@:1}"
do
	rm "/boot/vmlinuz-$ver"
	rm "/boot/initrd.img-$ver"
	rm "/boot/System.map-$ver"
	rm "/boot/config-$ver"
	rm -fr "/lib/modules/$ver"
	rm "/var/lib/initramfs-tools/$ver"
done
update-grub2
