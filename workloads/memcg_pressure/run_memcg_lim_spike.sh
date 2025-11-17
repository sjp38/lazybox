#!/bin/bash
#
# Run a command with memory cgroup that has specified memory limit and memory
# spike stress

if [ $# -ne 4 ]
then
	echo "Usage: $0 <mem limit in MiB> <spike size in MiB> \\"
	echo "		<spike interval (seconds)> <command>"
	exit 1
fi

BINDIR=$(dirname "$0")
cd "$BINDIR" || (echo 'failed moving to bindir'; exit 1)

MEMLIM=$(($1 * 1024 * 1024))
SZ_SPIKE=$2
SPIKE_INTERVAL=$3
COMM=$4

MEMCG_ORIG_DIR=/sys/fs/cgroup/memory/
MEMCG_DIR=/sys/fs/cgroup/memory/run_memcg_lim_$USER
sudo mkdir "$MEMCG_DIR"
sudo bash -c "echo $$ > $MEMCG_DIR/tasks"
sudo bash -c "echo $MEMLIM > $MEMCG_DIR/memory.limit_in_bytes"

./memcg_mspike.sh "$SZ_SPIKE" "$SPIKE_INTERVAL" &

echo "COMM: $COMM"

eval "$COMM"

killall memcg_mspike.sh



while read -r pid; do
	sudo bash -c "echo $pid > $MEMCG_ORIG_DIR/tasks"
done < "$MEMCG_DIR"/tasks

sudo rmdir "$MEMCG_DIR"
