# Cookbook Name:: openvpn
# Recipe:: peernode
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

include_recipe 'openvpn'

openvpn_conf_dir = node['openvpn']['conf_dir']

template "#{openvpn_conf_dir}/openvpn_inband.conf" do
  source "peernode/inband.conf.erb"
  mode "0600"
  owner "root"
  group "wheel"
  notifies :restart, "service[openvpn_inband]", :delayed
  variables(
    :openvpn_inband_port => node['openvpn']['inband_port'],
    :peernode_inband_ip => node['aw']['peernode_inband_ip'],
    :inband_mgmt_port => node['openvpn']['inband_mgmt_port'],
    :inband_interface => node['aw']['inband_interface']
  )
end

template "#{openvpn_conf_dir}/openvpn_outofband.conf" do
  source "peernode/outofband.conf.erb"
  mode "0600"
  owner "root"
  group "wheel"
  notifies :restart, "service[openvpn_outofband]", :delayed
  variables(
            :openvpn_outofband_port => node['openvpn']['outofband_port'],
            :outofband_mgmt_port => node['openvpn']['outofband_mgmt_port'],
            :outofband_interface => node['aw']['outofband_interface'],
            :rtkbox_outofband_ip => node['aw']['rtkbox_outofband_ip'],
            :peernode_outofband_ip => node['aw']['peernode_outofband_ip']
           )
end

#add pf.conf
cookbook_file '/etc/rc.conf.d/pf' do
  source 'rc.conf.d/pf.peernode'
  notifies :restart, "service[pf]", :delayed
end

template "#{node['pf']['conf_dir']}/pf.conf" do
  source "peernode/pf.conf.erb"
  mode "0600"
  owner "root"
  group "wheel"
  backup 5
  notifies :restart, "service[openvpn_inband]", :delayed
  variables(
            :inband_interface => node['aw']['inband_interface'],
            :rtkbox_inband_ip => node['aw']['rtkbox_inband_ip'],
            :peernode_ext_if => node['aw']['peernode_external_interface']
           )
  notifies :restart, "service[pf]", :delayed
end
