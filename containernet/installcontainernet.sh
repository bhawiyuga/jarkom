#!/bin/bash
echo "Install docker...."
curl -fsSL https://test.docker.com -o test-docker.sh
sudo sh test-docker.sh
sudo usermod -aG docker $(whoami)
newgrp docker
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
git pull https://github.com/bhawiyuga/jarkom.git
docker build -f ./jarkom/containernet/Dockerfile.ubuntu1804 -t containernet:ubuntu .
