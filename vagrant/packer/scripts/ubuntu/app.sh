#!/bin/bash

# ######################################################################
# DevOps: Htop, Nethogs
# ######################################################################
sudo apt-get install -qq build-essential software-properties-common
# Postgres
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
# Python
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo add-apt-repository ppa:fkrull/deadsnakes-python2.7
# Mosh
sudo add-apt-repository ppa:keithw/mosh
# Pypy
sudo add-apt-repository ppa:pypy/ppa
# Updates
sudo apt-get update
sudo apt-get install -y exuberant-ctags cmake libevent-dev libncurses5-dev
# Trusty doesn't come with Tmux 2.1, so we install it
# download and install Tmux from official http://tmux.github.io/ site
wget https://github.com/tmux/tmux/releases/download/2.1/tmux-2.1.tar.gz
tar xvf tmux-2.1.tar.gz
cd tmux-2.1 && ./configure && make && sudo make install
sudo apt-get install -qq ruby
sudo gem install tmuxinator
sudo apt-get install -qq htop
sudo apt-get install -qq nethogs


# ######################################################################
# Standard Packages
# ######################################################################
sudo apt-get install -qq git git-all


# Python
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo add-apt-repository ppa:fkrull/deadsnakes-python2.7
sudo apt-get update
# Python 2.7.11
sudo apt-get install -qq autotools-dev blt-dev bzip2 dpkg-dev g++-multilib gcc-multilib
sudo apt-get install -qq libbluetooth-dev libbz2-dev libexpat1-dev libffi-dev
sudo apt-get install -qq libffi6 libffi6-dbg libgpm2 libncursesw5-dev libreadline-dev
sudo apt-get install -qq libsqlite3-dev libssl-dev libtinfo-dev mime-support net-tools
sudo apt-get install -qq netbase python-crypto python-mox3 python-pil python-ply quilt
sudo apt-get install -qq tk-dev zlib1g-dev
sudo apt-get install -qq python2.7-dev

# Python 3.5.1
sudo apt-get install -qq python3.5 python3.5-dev

# Pypy
sudo apt-get install -qq gcc make libffi-dev pkg-config libz-dev libbz2-dev
sudo apt-get install -qq libsqlite3-dev libncurses-dev libexpat1-dev libssl-dev
sudo apt-get install -qq libgdbm-dev tk-dev liblzma-dev
sudo apt-get install -qq pypy pypy-dev

# sudo apt-get install -qq python-dev
sudo apt-get install -qq python-pip
sudo apt-get install -qq libffi-dev # for psycopg2_cffi
sudo apt-get install -qq libssl-dev
sudo apt-get install -qq libpq-dev # for psycopg2_cffi

# Update security to remove warnings and install base packages
sudo -H pip install --upgrade ndg-httpsclient urllib3[secure] pyasn1 certifi ipython
sudo -H pip install -U pip
sudo -H pip install virtualenv
sudo -H pip install --ignore-installed six virtualenvwrapper

wget -q https://bootstrap.pypa.io/get-pip.py
sudo -H python3.5 get-pip.py
sudo -H python3.5 -m pip install --upgrade ndg-httpsclient urllib3[secure] pyasn1 certifi ipython
sudo -H python3.5 -m pip install -U pip

sudo -H pypy get-pip.py
sudo -H pypy -m pip install --upgrade ndg-httpsclient urllib3[secure] pyasn1 certifi ipython
sudo -H pypy -m pip install -U pip
sudo -H pypy -m pip install git+https://bitbucket.org/pypy/numpy.git@pypy-4.0.1


# Mosh
sudo apt-get install -qq mosh

# Postgres
sudo apt-get install -qq postgresql-9.5

# Bottled Water
sudo apt-get install -qq cmake libsnappy-dev libjansson-dev libcurl4-openssl-dev
git clone https://github.com/confluentinc/bottledwater-pg.git
# (cd bottledwater-pg && make && sudo make install)

# Librdkafka
wget -O librdkafka-debian-0.8.6-1.tar.gz 'https://github.com/edenhill/librdkafka/archive/debian/0.8.6-1.tar.gz'
tar -xzf librdkafka-debian-0.8.6-1.tar.gz
(cd librdkafka-debian-0.8.6-1 && ./configure && make && sudo make install)


# ######################################################################
# Add Jenkins
# ######################################################################
wget -q -O - https://jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install -qq jenkins