#!/bin/bash

if [[ `uname -a` == "Darwin" ]];
then
  export ETHDEV="en0: Wi-Fi (AirPort)"
else
  export ETHDEV="eth0"
fi
alias crust="VAGRANT_CWD=$HOME/private/sandbox/crust vagrant"
