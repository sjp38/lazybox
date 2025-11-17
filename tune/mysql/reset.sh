#!/bin/bash

pushd /usr/local/mysql

sudo rm -fr data
sudo mkdir data
sudo chown -R mysql data
sudo -u mysql ./scripts/mysql_install_db --user=mysql

popd
