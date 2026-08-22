#!/bin/bash
# SPDX-License-Identifier: GPL-2.0

set -e

if [ $# -ne 3 ]
then
	echo "Usage: $0 <base img> <overlay disk> <disk size>"
	echo "E.g., $0 base.img overlay.disk 64G"
	exit 1
fi

base_img=$1
overlay_disk=$2
disk_sz=$3

qemu-img create -f qcow2 -b "$base_img" -F qcow2 "$overlay_disk" "$disk_sz"
cat <<EOF > user-data
#cloud-config
user: lazyvm
password: lazyvm
chpasswd:
  expire: False
ssh_pwauth: True
growpart:
  mode: auto
  devices: ['/']
  ignore_growroot: False
runcmd:
  - echo "lazy setup complete" > /etc/lazy_setup_complete
  - sync
  - poweroff
EOF

cat <<EOF > meta-data
isntance-id: lazyvm
local-hostname: lazyvm
EOF

cloud-localds seed.iso user-data meta-data

sudo qemu-system-x86_64 \
	-enable-kvm -cpu host -smp 2 -m 2G \
	-drive file="$overlay_disk",format=qcow2,if=virtio \
	-drive file="seed.iso",format=raw,if=virtio \
	-nographic -no-reboot

echo "Done.  Now you can start your VM using $overlay_disk."
echo "Remember you should keep base image together."
echo "seed.img, user-data and meta-data can be removed."
