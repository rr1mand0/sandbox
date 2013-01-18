# Cookbook Name:: packages
# Recipe:: default
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

packages_root = node['packages']['packages_root']
directory packages_root do
  owner "www-data"
  group "www-data"
  mode "0755"
  action :create
  recursive true
end

package_categories = node['packages']['package_categories']
for category in package_categories do
  directory "#{packages_root}/#{category}" do
    owner "www-data"
    group "www-data"
    mode "0755"
    action :create
  end
end

template '/etc/apache2/sites-available/aw-packages' do
  source 'etc/apache2/sites-available/aw-packages.erb'
  mode "0644"
  owner "root"
  group "root"
  notifies :reload, "service[apache2]", :delayed
  variables(
    :read_port => node['packages']['read_port'],
    :server_name => node['packages']['server_name'],
    :packages_root => packages_root,
    :read_user => node['packages']['read_user'],
    :ssl_cert => node['packages']['ssl_cert'],
    :ssl_key => node['packages']['ssl_key'],
    :ssl_ca_cert => node['packages']['ssl_ca_cert'],
    :write_port => node['packages']['write_port'],
    :write_user => node['packages']['write_user']
  )
end

execute "a2ensite aw-packages" do
  creates '/etc/apache2/sites-enabled/aw-packages'
  notifies :reload, "service[apache2]", :delayed
end

execute "a2enmod dav" do
  creates '/etc/apache2/mods-enabled/dav.load'
  notifies :restart, "service[apache2]", :delayed
end

execute "a2enmod dav_fs" do
  creates '/etc/apache2/mods-enabled/dav_fs.load'
  notifies :restart, "service[apache2]", :delayed
end

execute "a2enmod ssl" do
  creates '/etc/apache2/mods-enabled/ssl.load'
  notifies :restart, "service[apache2]", :delayed
end

service "apache2" do
  supports :status => true, :restart => true, :start => true, :reload => true
  action [:start]
end
