#
# Cookbook Name:: activemq
# Recipe:: rtkbox
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute
#

include_recipe 'activemq'

base_dir = node['activemq']['base_dir']
conf_dir = "#{base_dir}/conf"

Chef::Log.info("ActiveMQ RTKBox configuration.")
template "#{conf_dir}/activemq.xml" do
  source "rtkbox/activemq.xml.erb"
  mode "644"
  owner "activemq"
  group "activemq"
  notifies :restart, "service[activemq]"
end
