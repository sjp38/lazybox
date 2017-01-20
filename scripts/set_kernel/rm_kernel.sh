#!/bin/bash

if [ $# -ne 1 ];
then
	echo "Usage: $0 <target kernel version>"
	exit 1
fi

rm /boot/vmlinuz-$1
rm /boot/initrd.img-$1
rm /boot/System.map-$1
rm /boot/config-$1
rm -fr /lib/modules/$1
rm /var/lib/initramfs-tools/$1
update-grub2
