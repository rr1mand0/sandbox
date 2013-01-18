# Cookbook Name:: cassandra
# Recipe:: cassandra
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

#change this to normal user/group once this bug is resolved: http://tickets.opscode.com/browse/CHEF-3665
touch_file = node['cassandra']['user_created_flag']
test_cmd = "test `grep -c cassandra /etc/passwd` -eq 0"
group_add = "pw group add cassandra -g 2003"
user_add = "pw user add cassandra -u 2003 -c \"Cassandra\" -s /sbin/nologin -g cassandra -d \"\""
touch = "touch #{touch_file}"
execute "create user" do
    #test so we only run it if cassandra doesn't exist already else chef will throw an exception 
    command "#{test_cmd} && #{group_add} && #{user_add} && #{touch}"
    creates "#{touch_file}"
end


template '/etc/rc.conf.d/cassandra' do
  source 'rc.conf.d/cassandra.erb'
  mode "0640"
  owner "root"
  group "wheel"
  notifies :restart, "service[cassandra]", :delayed
  variables( :enable => node['cassandra']['enable_daemon'] )
end


data_dir = node['cassandra']['data_dir']
directory "#{data_dir}" do
    user "cassandra"
    group "cassandra"
    mode "0755"
    recursive true
end
log_dir = node['cassandra']['log_dir']
directory "#{log_dir}" do
    user "cassandra"
    group "cassandra"
    mode "0755"
end

template "/usr/local/etc/rc.d/cassandra" do
    source "rc.d/cassandra.erb"
    mode "0755"
    owner "root"
    group "wheel"
    notifies :restart, "service[cassandra]"
end

#config file
template "/usr/local/share/cassandra/conf/cassandra.yaml" do
    source "conf/cassandra.yaml.erb"
    mode "0644"
    owner "root"
    group "wheel"
    notifies :restart, "service[cassandra]", :delayed
    variables(
        :data_dir => data_dir
    )
end

template "/usr/local/share/cassandra/conf/cassandra-env.sh" do
    source "conf/cassandra-env.sh.erb"
    mode "0444"
    owner "root"
    group "wheel"
    notifies :restart, "service[cassandra]", :delayed
    variables(
        :max_heap_size => node['cassandra']['max_heap_size'],
        :heap_newsize => node['cassandra']['heap_newsize']
    )
end

service "cassandra" do
  supports :status => true, :restart => true, :start => true
  action [:start]
end

