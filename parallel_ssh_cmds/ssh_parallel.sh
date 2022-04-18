#!/bin/bash

pr_usage()
{
	echo "Usage: $0 [OPTION]... <cmd> <host>..."
	echo
	echo "OPTION"
	echo "  --port <port>		Specify the ssh port to use"
	echo "  --log_prefix <prefix>	Prefix of the log files"
	echo "  --keep_log		Keep log files"
	echo "  -h, --help		Show this usage"
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

ssh_port=22
log_prefix=""
keep_log="false"

while [ $# -ne 0 ]
do
	case $1 in
	"--port")
		if [ $# -lt 2 ]
		then
			pr_usage_exit 1
		fi
		ssh_port=$2
		shift 2
		continue
		;;
	"--log_prefix")
		if [ $# -lt 2 ]
		then
			pr_usage_exit 1
		fi
		log_prefix=$2
		shift 2
		continue
		;;
	"--keep_log")
		keep_log="true"
		shift 1
		continue
		;;
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
	if [ "$keep_log" = "true" ]
	then
		date_str=$(date +"%Y-%m-%d-%H-%M")
		log_file="$log_prefix"ssh_parallel_"$host"_"$date_str"
		log_file=$(mktemp "$log_file"_XXXX)
		ssh -p "$ssh_port" "$host" "$cmd" | tee "$log_file" &
	else
		ssh -p "$ssh_port" "$host" "$cmd" &
	fi
done

wait
