# Cookbook Name:: pkmtest
# Recipe:: default
#
# All rights reserved.

directory "#{node['pkmtest']['my_dir']}" do
  mode "0700"
  owner "root"
  group "wheel"
  action :create
  recursive true
end


template "#{node['pkmtest']['my_dir']}/my_config_file.txt" do
  source "my_config_file.txt.erb"
  mode "0600"
  owner "root"
  group "wheel"
  variables( 
            :attrib1 => node['pkmtest']['attrib1'],
            :attrib2 => node['pkmtest']['attrib2']
           )
end
