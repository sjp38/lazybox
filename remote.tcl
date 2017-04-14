proc remote_sudocmd {username target ssh_port password cmds} {
	spawn ssh -t -p $ssh_port $username@$target sudo -- bash -c '$cmds'

	# for ssh password
	expect "*password*"
	send "$password\r"

	# for sudo command
	expect "*password*"
	send "$password\r"

	# wait for completion of ssh
	expect eof
}
