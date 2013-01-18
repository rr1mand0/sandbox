# Cookbook Name:: aw
# Recipe:: devtools
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

node['aw']['devtools'].each do |pkg|
  package pkg
end
