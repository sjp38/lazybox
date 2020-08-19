#!/bin/bash

WORKING_DIR=$(dirname "$0")

echo "[[ kernbuild start ]]"
echo "kernel version: $(uname -r)"
echo "kernel param: \"$(cat /proc/cmdline)\""
echo "date: $(date)"
echo ""

pushd "$WORKING_DIR"

KSRC_FTP_DIR="http://ftp.kernel.org/pub/linux/kernel/v4.x/"
KVER="linux-4.0"
KSRC_FILE=$KVER".tar.xz"
KSRC_FTP=$KSRC_FTP_DIR$KSRC_FILE
if [ ! -f $KSRC_FILE ]
then
	echo "curl $KSRC_FTP > $KSRC_FILE"
	curl "$KSRC_FTP" > "$KSRC_FILE"
	echo "curled!"
fi

if [ ! -d build_dir ]
then
	mkdir build_dir
	tar Jxf $KSRC_FILE -C build_dir/
fi

NR_CPU=$(grep -c "processor" /proc/cpuinfo)

pushd build_dir/$KVER

make distclean
make defconfig
echo 3 > /proc/sys/vm/drop_caches
( /usr/bin/time make -sj $((NR_CPU * 4)) ) 2>&1

popd
popd
echo "[[ Test Done ]]"
