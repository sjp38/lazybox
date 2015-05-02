#!/usr/bin/expect --
set timeout -1

# Do experiments from remote target machine using run_exps.py
# lazybox should be installed on remote target machine.
#
# Usage:
# expect remote_exps.exp <username> <target> <ssh port> <password> \
#                           <lazybox path> <exp>

if { [llength $argv] < 6 } {
	puts "usage: "
	puts "expect remote_exps.exp \\"
        puts "              <username> <target> <ssh port> <password> \\"
        puts "              <lazybox path> <exp>"
	exit 1
}

set username [lindex $argv 0]
set target [lindex $argv 1]
set ssh_port [lindex $argv 2]
set password [lindex $argv 3]
set lbpath [lindex $argv 4]
set exp [lindex $argv 5]

# login
spawn ssh -p $ssh_port $username@$target
expect -re "password"
send "$password\r"
expect -re "$target"

# be su
send "sudo su\r"
expect -re "password"
send "$password\r"
expect -re "$target"

# move to and do experiment
send "pushd $lbpath\r"
expect -re "$target"
send "./run_exps.py $exp\r"
expect -re "$target"

send "popd\r"
expect -re "$target"
