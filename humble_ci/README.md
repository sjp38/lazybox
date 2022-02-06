Humble Contiguous Integration
=============================

This directory contains a script for simple contiguous integration works.  The
script periodically checks if specific git repo has updated and runs
user-specified tasks for each of the updates.  The script saves the state of
each task and continues the tasks from the last saved position when executed
again, so fault-tolerant.  This feature makes it useful to be used by tasks
that could kill the script, e.g., kernel installation and reboot.

The tasks could be specified as a list of commands.  The commands can know for
what source tree it has triggered via following environmental variables.

- HUMBLE_CI_REPO: Path to the git repo
- HUMBLE_CI_BRANCH: Branch that updated
- HUMBLE_CI_REMOTE: Name of the remote of the branch
- HUMBLE_CI_URL: Url of the remote

If any of the tasks fail, the tasks are marked as failed and no subsequent
tasks be executed.
