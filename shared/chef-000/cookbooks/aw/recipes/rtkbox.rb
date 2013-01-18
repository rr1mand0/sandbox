# Cookbook Name:: aw
# Recipe:: rtkbox
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

include_recipe 'aw'

aw_etc_dir = node['aw']['etc_dir']
cookbook_file aw_etc_dir + '/rtk_config.json' do
  source 'etc/rtkbox.rtk_config.json'
  mode "0644"
  owner "root"
  group "wheel"
  for service_name in node['aw']['services'] do
    notifies :restart, "service[#{service_name}]", :delayed
  end
end
