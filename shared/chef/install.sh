#!/bin/bash

# This runs as root on the server
# ./install.sh chef_json_file.json

chef_binary=/var/lib/gems/1.9.1/gems/chef-0.10.4/bin/chef-solo

# Are we on a vanilla system?
if ! test -f "$chef_binary"; then
    export DEBIAN_FRONTEND=noninteractive
    # Upgrade headlessly (this is only safe-ish on vanilla systems)
    apt-get update &&
    apt-get -o Dpkg::Options::="--force-confnew" \
        --force-yes -fuy dist-upgrade &&
    # Install Ruby and Chef
    apt-get install -y ruby1.9.1 ruby1.9.1-dev make &&
    sudo gem1.9.1 install --no-rdoc --no-ri chef --version 0.10.4
fi &&

"$chef_binary" -c solo.rb -j solo.json
