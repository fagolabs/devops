#!/bin/bash

apt-get install -y python-pip python-setuptools libssl-dev libffi-dev openssl
pip install --upgrade requests
pip install cryptography pyOpenSSL pynacl bcrypt
