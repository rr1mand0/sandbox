#
# Cookbook Name:: crust
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#


base_packages = {
  'python-dev' => nil,
  'python-pip' => nil,
  'python-django' => nil
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

