#!/bin/bash
set -xe
source retry.sh

retry_10_times_sleep_5 apt update

#python
retry_10_times_sleep_5 apt install -yqq python3.8 python3.8-distutils python3.8-dev \
python3.8-testsuite python3.8-stdlib python3.8 python3.8-venv python3-venv
sudo rm -rf /usr/bin/python
sudo ln /usr/bin/python3.8 /usr/bin/python

#pip
sudo apt install python3-pip -y
pip3 install --upgrade pip

#setuptools
pip3 install --upgrade setuptools

#git
sudo apt install git -y

#make
sudo apt install make -y

cd /opt

#horey
sudo rm -rf horey
sudo git clone https://github.com/AlexeyBeley/horey.git
sudo chown -R  ubuntu:ubuntu horey/
cd horey
make recursive_install_from_source-provision_constructor
