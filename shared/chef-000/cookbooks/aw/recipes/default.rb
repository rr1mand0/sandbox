# Cookbook Name:: aw
# Recipe:: default
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

include_recipe 'aw::dependency_pkgs'

aw_etc_dir = node['aw']['etc_dir']
directory aw_etc_dir do
  owner "root"
  group "wheel"
  mode "0755"
  action :create
  recursive true
end

package_cache = node['aw']['package_cache']
directory ::File.dirname(package_cache) do
  owner "root"
  group "wheel"
  mode "0755"
  action :create
  recursive true
end

cookbook_file package_cache do
  source 'aw.tbz'
end

aw_services = node['aw']['services']
aw_package 'aw' do
  package_cache package_cache
  packages_url node['aw']['packages_url']
  packages_category node['aw']['packages_category']
  client_key 'packaging_client.key.pem'
  client_cert 'packaging_client.cert.pem'
  ca_cert 'cloud.arcticwolf.biz-CA.cert.pem'
  package_version node['aw']['package_version']
  enable_upgrade node['aw']['enable_upgrade']
  always_upgrade node['aw']['always_upgrade']
  for service_name in aw_services do
    notifies :restart, "service[#{service_name}]", :delayed
  end
  # TODO broadcast to adjacent nodes that we've upgraded from version X => Y
  # TODO kick off an iteration of the monitoring client
end

group 'rtkwlf' do
  gid node['aw']['rtkwlf_gid']
end

aw_root_dir = node['aw']['root_dir']
user 'rtkwlf' do
  comment "Fenrir"
  uid node['aw']['rtkwlf_uid']
  gid node['aw']['rtkwlf_gid']
  home aw_root_dir
  shell node['aw']['rtkwlf_shell']
  password "*"
end

# FIXME don't have rtkwlf in wheel group
execute "pw groupmod wheel -m rtkwlf" # will only add if not already a member

rtkwlf_dot_ssh = "#{aw_root_dir}/.ssh"
directory rtkwlf_dot_ssh do
  owner 'root'
  group 'wheel'
  mode '0755'
end

# Generate rtkwlf's authorized_keys file
# FIXME don't allow passwordless SSH
rtkwlf_authorized_keys = "#{rtkwlf_dot_ssh}/authorized_keys"
if !::File.exists?(rtkwlf_authorized_keys)
  for authorized_keys_file in [ '/root/.ssh/authorized_keys', '/home/vagrant/.ssh/authorized_keys' ] do
    if ::File.exists?(authorized_keys_file)
      Chef::Log.info("Copying #{authorized_keys_file} into rtkwlf's authorized_keys")
      execute "cat #{authorized_keys_file} >>#{rtkwlf_authorized_keys}"
    end
  end
end

file rtkwlf_authorized_keys do
  mode '0644'
  owner 'root'
  group 'wheel'
end

aw_log_dir = node['aw']['log_dir']
directory aw_log_dir do
  owner "root"
  group "rtkwlf"
  mode "4775"
  action :create
  recursive false
end

if ::File.exists?(aw_log_dir)
  ::Dir.foreach(aw_log_dir) do |item|
    next if item == '.' or item == '..'
    file "#{aw_log_dir}/#{item}" do
      mode '0664'
      owner 'root'
      group 'rtkwlf'
    end
  end
end

# Configure AW services
aw_rc_d_dir = node['aw']['rc.d_dir']
rc_conf_dir = node['aw']['rc.conf.d_dir']
for service_name in aw_services
  cookbook_file "#{aw_rc_d_dir}/#{service_name}" do
    source "rc.d/#{service_name}"
    mode "0555"
    owner "root"
    group "wheel"
    notifies :restart, "service[#{service_name}]", :delayed
  end

  service service_name do
    supports :status => true, :restart => true, :start => true
  end

  cookbook_file "#{rc_conf_dir}/#{service_name}"  do
    source "rc.conf.d/#{service_name}"
    mode "0644"
    owner "root"
    group "wheel"
    notifies :restart, "service[#{service_name}]", :delayed
  end
end
