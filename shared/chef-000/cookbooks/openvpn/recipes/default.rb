# Cookbook Name:: openvpn
# Recipe:: default
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

openvpn_conf_dir = node['openvpn']['conf_dir']
openvpn_rc_dir = node['openvpn']['rc_dir']
rc_conf_dir = '/etc/rc.conf.d'

directory "#{openvpn_conf_dir}" do
    mode "0700"
    owner "root"
    group "wheel"
    action :create
end

template "#{openvpn_rc_dir}/openvpn_inband" do
    source "rc.d/openvpn.erb"
    mode "0755"
    owner "root"
    group "wheel"
    variables( :service => 'openvpn_inband' )
    notifies :restart, "service[openvpn_inband]", :delayed
end

template "#{openvpn_rc_dir}/openvpn_outofband" do
    source "rc.d/openvpn.erb"
    mode "0755"
    owner "root"
    group "wheel"
    variables( :service => 'openvpn_outofband' )
    notifies :restart, "service[openvpn_outofband]", :delayed
end

#startup var's
directory rc_conf_dir do
    mode "0755"
    owner "root"
    group "wheel"
    action :create
end

template "#{rc_conf_dir}/openvpn_inband" do
    source "rc.conf.d/openvpn_inband"
    mode "0644"
    owner "root"
    group "wheel"
    variables( :enable => node['openvpn']['inband_enable'] )
    notifies :restart, "service[openvpn_inband]", :delayed
end
template "#{rc_conf_dir}/openvpn_outofband" do
    source "rc.conf.d/openvpn_outofband"
    mode "0644"
    owner "root"
    group "wheel"
    variables( :enable => node['openvpn']['outofband_enable'] )
    notifies :restart, "service[openvpn_inband]", :delayed
end

#TODO: we shouldn't be deploying the key like this
template "#{openvpn_conf_dir}/static.key" do
    source "static.key"
    mode "0600"
    owner "root"
    group "wheel"
    notifies :restart, "service[openvpn_inband]", :delayed
    notifies :restart, "service[openvpn_outofband]", :delayed
end

cookbook_file '/etc/rc.conf.d/routing' do
  source 'rc.conf.d/routing'
  mode "0644"
  notifies :run, "execute[ip_forwarding]"
end

service "openvpn_inband" do
  supports :start => true, :restart => true, :status => true
end

service "openvpn_outofband" do
  supports :start => true, :restart => true, :status => true
end

service "pf" do
  supports :start => true, :restart => true, :status => true
end

execute "ip_forwarding" do
  command "sysctl -w net.inet.ip.forwarding=1"
  action :nothing
end
