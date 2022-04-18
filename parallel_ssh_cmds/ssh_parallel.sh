#!/bin/bash

pr_usage()
{
	echo "Usage: $0 [OPTION]... <cmd> <host>..."
	echo
	echo "OPTION"
	echo "  -h, --help	Show this usage"
}

pr_usage_exit()
{
	exit_code=$1
	pr_usage
	exit "$exit_code"
}

if [ $# -lt 1 ]
then
	pr_usage_exit 1
fi

while [ $# -ne 0 ]
do
	case $1 in
	"--help" | "-h")
		pr_usage_exit 0
		;;
	*)
		if [ $# -lt 2 ]
		then
			pr_usage_exit 1
		fi
		cmd=$1
		hosts=( "$@" )
		unset hosts[0]
		break;;
	esac
done

for host in ${hosts[@]}
do
	ssh "$host" "$cmd" &
done

wait
