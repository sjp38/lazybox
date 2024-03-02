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

proc remote_sudocmd_registered {username target ssh_port password cmds} {
	spawn ssh -t -p $ssh_port $username@$target sudo -- bash -c '$cmds'

	# for sudo command
	expect "*password*"
	send "$password\r"

	# wait for completion of ssh
	expect eof
}

proc remote_sudoercmd {username target ssh_port password cmds} {
	remote_cmd_n_password $username $target $ssh_port $password $cmds 1
}

# Do remote command which requires n-time password input
proc remote_cmd_n_password {username target ssh_port password cmds nr_prompt} {
	spawn ssh -t -p $ssh_port $username@$target bash -c '$cmds'

	# for ssh password
	expect "*password*"
	send "$password\r"

	set i 0
	while {$i < $nr_prompt} {
		puts "$i prompt"
		expect "*password*"
		send "$password\r"
		incr i
	}

	# wait for completion of ssh
	expect eof
}
