#!/bin/bash
echo "Install containernet...."
sudo apt update
sudo apt -y install ansible git aptitude
git clone https://github.com/containernet/containernet.git
cd containernet/ansible
sudo ansible-playbook -i "localhost," -c local install.yml
cd ..
sudo make develop
echo "Building docker image...."
cd ~
git clone https://github.com/bhawiyuga/jarkom.git
cd ~/jarkom/containernet/
docker build -f Dockerfile.ubuntu1804 -t containernet:bionic .
cd ~
