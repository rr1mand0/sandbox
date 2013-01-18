#
# Cookbook Name:: activemq
# Recipe:: default
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute
#

#package "activemq" do
##    version "5.5.0"
##    action :install
##end


base_dir = node['activemq']['base_dir']
conf_dir = "#{base_dir}/conf"
data_dir = node['activemq']['data_dir']
rc_conf_dir = node['activemq']['rc_conf_dir']

template "#{rc_conf_dir}/activemq" do
    source "rc.conf.d/activemq.erb"
    mode "0755"
    owner "root"
    group "wheel"
end

#default activemq install is broken, /usr/local/activemq/data is a link to nowhere.
#move it to /var/activemq
directory "#{data_dir}" do
    mode "0755"
    owner "activemq"
    group "activemq"
    action :create
end
cookbook_file "/tmp/fix_activemq_data_link.sh" do
    source "fix_activemq_data_link.sh"
    mode "755"
    action :create
end
#NOTE: the command is supposed to override the name here but that doesn't actually work so
#we specify the command as the name. wtf.
execute "/tmp/fix_activemq_data_link.sh && touch #{base_dir}/.datalnfix" do
    command = "/tmp/fix_activemq_data_link.sh && touch #{base_dir}/.datalnfix"
    action :run
    creates "#{base_dir}/.datalnfix"
    notifies :restart, "service[activemq]"
end

#clean out the conf directory to get rid of all the cruft
execute "rm -r #{conf_dir}/* && touch #{base_dir}/.cleanconf" do
    command = "rm -r #{conf_dir}/* && touch #{base_dir}/.cleanconf"
    action :run
    creates "#{base_dir}/.cleanconf"
end

#rebuild the config files
template "#{conf_dir}/camel.xml" do
    source "common/camel.xml.erb"
    mode "644"
    owner "activemq"
    group "activemq"
    notifies :restart, "service[activemq]"
end
template "#{conf_dir}/credentials.properties" do
    source "common/credentials.properties.erb"
    mode "644"
    owner "activemq"
    group "activemq"
    notifies :restart, "service[activemq]"
end
template "#{conf_dir}/jetty-realm.properties" do 
    source "common/jetty-realm.properties.erb" 
    mode "644"
    owner "activemq"
    group "activemq"
    notifies :restart, "service[activemq]"
end
template "#{conf_dir}/jetty.xml" do
    source "common/jetty.xml.erb"
    mode "644"
    owner "activemq"
    group "activemq"
    notifies :restart, "service[activemq]"
end
template "#{conf_dir}/log4j.properties" do
    source "common/log4j.properties.erb"
    mode "644"
    owner "activemq"
    group "activemq"
    notifies :restart, "service[activemq]"
end

service "activemq" do
    supports :start => true, :restart => true
end
