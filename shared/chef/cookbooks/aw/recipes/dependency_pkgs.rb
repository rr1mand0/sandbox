# Cookbook Name:: aw
# Recipe:: dependency_pkgs
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

node['aw']['dependency_packages'].each do |pkg|
  package pkg
end

node['aw']['dependency_pips'].each do |pip|
  execute "pip-2.7 -q install #{pip}"
end
