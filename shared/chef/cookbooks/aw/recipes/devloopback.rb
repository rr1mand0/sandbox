# Cookbook Name:: aw
# Recipe:: devloopback
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

if !node['network']['interfaces'].has_key?('lo1')
  execute 'ifconfig lo1 create'
  execute 'ifconfig lo1 10.8.9.33/32 up'
  execute 'ifconfig lo1 10.8.9.44/32 alias' 
  execute 'ifconfig lo1 10.8.9.55/32 alias'
end
