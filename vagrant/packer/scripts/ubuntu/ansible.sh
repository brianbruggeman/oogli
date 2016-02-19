#!/bin/bash -eux

# Install Ansible repository.
apt-get -qq install software-properties-common
apt-add-repository ppa:ansible/ansible

# Install Ansible.
apt-get -qq update
apt-get -qq install python python-pip ansible

# Post installation
mkdir /tmp/packer-provisioner-ansible-local
chmod 777 /tmp/packer-provisioner-ansible-local
