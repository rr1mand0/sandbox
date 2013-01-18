# Author:: Peter McAlpine (<peter.mcalpine@arcticwolf.com>)
# Cookbook Name:: pkmtest
# Attributes:: default
#
# All rights reserved.

require 'rbconfig'

default['pkmtest']['my_dir']          = '/deleteme/pkmtest'

default["pkmtest"]["attrib1"]         = "-1"

case platform
when "freebsd"
  default["pkmtest"]["attrib1"]       = "1"
  default["pkmtest"]["attrib2"]       = "2"
else
  raise "Uh oh! Invalid platform (default): #{platform}"
end
