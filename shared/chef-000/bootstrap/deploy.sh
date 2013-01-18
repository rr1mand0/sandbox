#!/bin/bash -x

# Usage: ./deploy.sh [host]

host="${1:-precise64@arcticwolf.com}"

# The host key might change when we instantiate a new VM, so
# we remove (-R) the old host key from known_hosts
#ssh-keygen -R "${host#*@}" 2> /dev/null

tar cj . | ssh "$host" '
sudo rm -rf ~/chef &&
mkdir ~/chef &&
cd ~/chef &&
tar xj &&
sudo bash install.sh'
