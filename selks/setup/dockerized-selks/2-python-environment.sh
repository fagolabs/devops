#!/bin/bash

# Install dependencies + docker-compose 
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip python-setuptools libssl-dev libffi-dev openssl
pip install --upgrade requests
pip install cryptography pyOpenSSL pynacl bcrypt
pip install docker docker-py
pip install docker-compose==1.9.0

# Configure memory footprint for docker-container
if ! grep -q "vm.max_map_count" /etc/sysctl.conf; then
   echo vm.max_map_count=262144 >> /etc/sysctl.conf
fi
sysctl -p
