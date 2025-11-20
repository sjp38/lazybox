Humble Contiguous Integration
=============================

This directory contains scripts for simple contiguous integration works.  The
main script, `hci.py`, can be used for periodically checking if specific git
repo has updated and running specific tasks for each of the updates.  The
script saves the state of each task and continues the tasks from the last saved
position when executed again, so fault-tolerant.  This feature makes it useful
to be used by tasks that could kill the script, e.g., reboot.

The tasks could be specified as a list of commands.  To let the commands know
for what source tree's update it has triggered, `hci.py` sets following
environmental variables.

- HUMBLE_CI_REPO: Path to the git repo
- HUMBLE_CI_BRANCH: Branch that updated
- HUMBLE_CI_REMOTE: Name of the remote of the branch
- HUMBLE_CI_URL: Url of the remote

If any of the tasks fails, the tasks are marked as failed and no subsequent
tasks will be executed.

Simple Update Notification Example
----------------------------------

You may use `hci.py` for getting simple upstream tree update notifications.
For the case, this directory contains a script for that purpose, namely
`noti_update.sh`.  It receives and email address to send the notirication,
formats the notirication message with the `HUMBLE_CI_*` environment variables,
and send the message via `git send-email`.  In other words, it assumes the user
would already set `git-sendemail` with smtp password so that it can send email
without intervention, and called by `hci.py`.

For example, below command will check updates to Linux mainline and two latest
LTS kernels for every hour, and send notice email.

    $ ./hci.py --repo ./linux \
               --tree_to_track linus git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git master \
               --tree_to_track stable git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git linux-6.6.y \
               --tree_to_track stable git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git linux-6.12.y \
               --cmds "./noti_update.sh $email_to_receive_noti" --delay 3600
