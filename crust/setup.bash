#!/bin/bash

if [[ `uname` == "Darwin" ]];
then
  export ETHDEV="en0: Wi-Fi (AirPort)"
else
  export ETHDEV="eth0"
fi
echo "ETHDEV=$ETHDEV"
alias crust="VAGRANT_CWD=$HOME/private/sandbox/crust vagrant"
