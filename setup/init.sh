#!/bin/bash

pip3 install virtualenv
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/munki:/Users/$USER/Library/Python/3.7/bin"
virtualenv -p /usr/bin/python3 ./venv
source ./venv/bin/activate