#!/bin/bash -eux

# Install Ansible repository.
apt-get -qq install software-properties-common
apt-add-repository ppa:ansible/ansible
apt-add-repository ppa:fkrull/deadsnakes-python2.7
apt-add-repository ppa:fkrull/deadsnakes

# Install Ansible.
apt-get -qq update
apt-get -qq install python python-dev python3.5 python3.5-dev python-pip ansible

# Post installation
mkdir /tmp/packer-provisioner-ansible-local
chmod 777 /tmp/packer-provisioner-ansible-local
