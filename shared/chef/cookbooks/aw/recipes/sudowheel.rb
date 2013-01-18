# Cookbook Name:: aw
# Recipe:: sudowheel
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

template node['sudo']['sudoers_file'] do
  source 'usr/local/etc/sudoers.erb'
  mode "0440"
  owner "root"
  group "wheel"
  variables( :enable => node['sudo']['sudowheel_enable'] )
end
