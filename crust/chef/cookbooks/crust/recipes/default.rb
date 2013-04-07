#
# Cookbook Name:: crust
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#


base_packages = {
  'libmysqlclient-dev' => nil,
  'mysql-client' => nil,
  'python-dev' => nil,
  'python-django' => nil,
  'python-django-south' => nil,
  'python-mysql.connector' => nil,
  'python-mysqldb' => nil,
  'python-pip' => nil,
  'python-setuptools' => nil,
  'python-simplejson' => nil,
  'python-tz' => nil,
  'vim' => nil
}

base_packages.each_pair do |package, ver|
  if ver.nil?
    package package
  else
    package package do
      action :install
      version ver 
    end
  end
end


cookbook_file "/etc/network/interfaces" do
  source "etc/network/interfaces"
  mode "0644"
  owner "root"
  group "root"
  notifies :restart, "service[networking]", :immediate
end

service "networking" do
  supports :start => true, :restart => true, :status => true
end

template "/etc/apache2/sites-available/crust" do
  source "etc/apache2/sites-available/crust.erb"
  mode "0644"
  owner "root"
  group "root"
  variables(
    :crust_root_dir      => node['crust']['crust_root_dir'],
    :crust_servername    => node['crust']['crust_servername'],
    :crust_admin_email   => node['crust']['crust_admin_email']
      )
  notifies :reload, "execute[a2ensite crust]", :delayed
end

execute "a2ensite crust" do
  notifies :reload, "service[apache2]", :delayed
end

service "apache2" do
  supports :start => true, :restart => true, :status => true
end

#www "crustydb" do
  #action :create
#end
