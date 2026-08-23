Getting Started
===============

Below commands will start a Debian 13 VM.

```
$ ./_install_deps.sh
$ ./_download_base_img.sh debian13 base.img
$ ./_mk_overlay_disk.sh base.img overlay.disk 8G
$ ./start_vm.py
```

The VM has an account of name lazyvm.  The password is same to the name.  Ssh
is also available via port 2242.
