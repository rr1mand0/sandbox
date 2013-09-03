#!/bin/bash

if [[ `uname` == "Darwin" ]];
then
  export ETHDEV="en0: Wi-Fi (AirPort)"
  export CRUST_MAC="080027880CA6"
else
  export ETHDEV="eth0"
  export CRUST_MAC="080027880CA7"
  export PLEX_MAC="080027880CA8"
fi
echo "ETHDEV=$ETHDEV"
alias crust="VAGRANT_CWD=$HOME/private/sandbox/crust vagrant"
