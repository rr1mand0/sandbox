# Cookbook Name:: openvpn
# Recipe:: rtkbox
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

include_recipe 'openvpn'

peernode_public_ip = node['aw']['peernode_public_ip']
if !peernode_public_ip
  raise "['aw']['peernode_public_ip'] attribute not set. Cannot configure openvpn."
end

openvpn_conf_dir = node['openvpn']['conf_dir']
inband_interface = node['aw']['inband_interface']
outofband_interface = node['aw']['outofband_interface']
rtkbox_inband_ip = node['aw']['rtkbox_inband_ip']

bridge_interface = node['aw']['rtkbox_bridge_interface']
bridged_interfaces = node['aw']['rtkbox_bridged_interfaces']
bridge_ip = node['aw']['rtkbox_bridge_ip']
if !node['network']['interfaces'].has_key?(bridge_interface)
  execute 'ifconfig bridge0 create'
  cmd = 'ifconfig bridge0'
  bridged_interfaces.each do |iface|
    cmd = cmd + " addm #{iface}"
  end
  execute cmd + ' up'
  bridged_interfaces.each do |iface|
    execute "ifconfig #{iface} up"
  end
  execute "ifconfig bridge0 inet #{bridge_ip}"
end

if !node['network']['interfaces'].has_key?(inband_interface)
  execute "ifconfig #{inband_interface} create" do
    notifies :restart, "service[openvpn_inband]", :delayed
  end
  execute "ifconfig #{inband_interface} #{rtkbox_inband_ip}" do
    notifies :restart, "service[openvpn_inband]", :delayed
  end
end

template "#{openvpn_conf_dir}/openvpn_inband.conf" do
  source "rtkbox/inband.conf.erb"
  mode "0600"
  owner "root"
  group "wheel"
  notifies :restart, "service[openvpn_inband]", :delayed
  variables(
            :peernode_public_ip => peernode_public_ip,
            :openvpn_inband_port => node['openvpn']['inband_port'],
            :rtkbox_inband_ip => rtkbox_inband_ip,
            :inband_mgmt_port => node['openvpn']['inband_mgmt_port'],
            :vpn_up => "#{openvpn_conf_dir}/vpn_up.sh",
            :vpn_down => "#{openvpn_conf_dir}/vpn_down.sh",
            :inband_interface => inband_interface
           )
end

cookbook_file "#{openvpn_conf_dir}/vpn_up.sh" do
  source 'rtkbox/vpn_up.sh'
  mode "0755"
  owner "root"
  group "wheel"
  notifies :restart, "service[openvpn_inband]", :delayed
end

cookbook_file "#{openvpn_conf_dir}/vpn_down.sh" do
  source 'rtkbox/vpn_down.sh'
  mode "0755"
  owner "root"
  group "wheel"
  notifies :restart, "service[openvpn_inband]", :delayed
end

template "#{openvpn_conf_dir}/openvpn_outofband.conf" do
  source "rtkbox/outofband.conf.erb"
  mode "0600"
  owner "root"
  group "wheel"
  notifies :restart, "service[openvpn_outofband]", :delayed
  variables(
            :peernode_public_ip => peernode_public_ip,
            :outofband_interface => outofband_interface,
            :openvpn_outofband_port => node['openvpn']['outofband_port'],
            :outofband_mgmt_port => node['openvpn']['outofband_mgmt_port'],
            :peernode_outofband_ip => node['aw']['peernode_outofband_ip'],
            :rtkbox_outofband_ip => node['aw']['rtkbox_outofband_ip']
           )
end

template "#{node['pf']['conf_dir']}/pf.conf" do
  source "rtkbox/pf.conf.erb"
  mode "0600"
  owner "root"
  group "wheel"
  backup 5
  variables(
    :peernode_public_ip => peernode_public_ip,
    :peernode_inband_ip => node['aw']['peernode_inband_ip'],
    :bridge_interface => node['aw']['rtkbox_bridge_interface'],
    :inband_interface => inband_interface,
    :outofband_interface => outofband_interface
  )
  notifies :restart, "service[pf]", :delayed
end

#add pf.conf
cookbook_file '/etc/rc.conf.d/pf' do
  mode "0644"
  source 'rc.conf.d/pf.rtkbox'
  notifies :restart, "service[pf]", :delayed
end
