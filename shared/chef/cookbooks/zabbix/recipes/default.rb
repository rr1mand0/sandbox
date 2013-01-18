#
# Cookbook Name:: zabbix-agent
# Recipe:: default
#
# Copyright 2012, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

#HACK! the pw provider (Chef::Provider::User::Pw) is broken on FreeBSD, as it attempts to set the password
#every time chef runs, and if it's blank it throws an exception and fails. Case CHEF-3665 has been opened:
#http://tickets.opscode.com/browse/CHEF-3665
#
#In the meantime we have to create the user manually. 

#group "zabbix" do
#    gid "2002"
#    action [:create, :modify]
#end

#user "zabbix" do
#    comment "Zabbix"
#    uid "2002"
#    gid "zabbix"
#    shell "/sbin/nologin"
#    home ""
#    password ""
#    #action [:create, :modify]
#    action :create
#end

#touch_file = "/usr/local/etc/zabbix2/.usercreated"
#test_cmd = "test `grep -c zabbix /etc/passwd` -eq 0"
#group_add = "pw group add zabbix -g 2002"
#user_add = "pw user add zabbix -u 2002 -c \"Zabbi \" -s /sbin/nologin -g zabbix -d \"\""
#touch = "touch #{touch_file}"
#execute "create user" do
#    #test so we only run it if zabbix doesn't exist already else chef will throw an exception 
#    command "#{test_cmd} && #{group_add} && #{user_add} && #{touch}"
#    creates "#{touch_file}"
#end

log_path = node['zabbix']['log_path']
directory "#{log_path}" do
    owner "zabbix"
    group "zabbix"
    mode "0755"
    action :create
end

