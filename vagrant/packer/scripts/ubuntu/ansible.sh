#!/bin/bash -eux

# Install Ansible repository.
apt-get -qq install software-properties-common
apt-add-repository ppa:ansible/ansible

# Install Ansible.
apt-get -qq update
apt-get -qq install ansible