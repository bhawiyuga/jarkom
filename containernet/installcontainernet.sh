#!/bin/bash
curl -fsSL https://test.docker.com -o test-docker.sh
sh test-docker.sh
sudo usermod -aG docker $(whoami)
sudo apt update
sudo apt -y install ansible git aptitude
git clone https://github.com/containernet/containernet.git
cd containernet/ansible
sudo ansible-playbook -i "localhost," -c local install.yml
cd ..
sudo make develop
