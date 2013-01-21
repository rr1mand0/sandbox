
#
# Cookbook Name:: pxe
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

package "dnsmasq"
package "apache2"


template "/etc/network/interfaces" do
    mode 0644
    source 'interfaces.erb'
    notifies :restart, "service[networking]"
end

template "/etc/dnsmasq.aw" do
    mode 0644
    source 'aw.erb'
    notifies :restart, "service[dnsmasq]"
end

template "/etc/default/dnsmasq" do
    mode 0644
    source 'dnsmasq.erb'
    notifies :restart, "service[dnsmasq]"
end

service "networking" do
  supports :start => true, :restart => true, :status => true
end

template "/etc/NetworkManager/NetworkManager.conf" do
    mode 0644
    source 'NetworkManager.conf.erb'
    notifies :run, "execute[restart-NetworkingManager]", :immediately
#notifies :run, "execute[reconfigure-chef-server]", :immediately
    
end

#template "/etc/sysctl.conf" do
#    mode 0644
#    source "sysctl.conf.erb"
#    notifies :restart, "script[sysctl.conf]"
#end

#ruby_block "allow ip_forwarding" do
# block do
#   fe = Chef::Util::FileEdit.new("/etc/sysctl.conf")
#   fe.insert_line_if_no_match("/^net.ipv4.ip_forward=1", "net.ipv4.ip_forward=1")
#   fe.write_file
# end
#not_if { Resolv.getaddress(node['chef-server']['api_fqdn']) rescue false } # host resolves
#end

script "sysctl.conf" do
  interpreter "bash"
  user "root"
  code <<-EOH
    echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/60.chef-pxe-server.conf
    iptables -F
    iptables -X
    iptables -t nat -F
    iptables -t nat -X
    iptables -t mangle -F
    iptables -t mangle -X
    iptables -t raw -F
    iptables -t raw -X
    iptables -A FORWARD -i eth1 -s 192.168.1.0/255.255.255.0 -j ACCEPT
    iptables -A FORWARD -i eth0 -d 192.168.1.0/255.255.255.0 -j ACCEPT
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
  EOH
  notifies :start, "service[procps]"
end

service "procps"

service "dnsmasq" do
  supports :start => true, :restart => true, :status => true
end

execute "restart-NetworkingManager" do
  command "restart network-manager &"
  action :nothing
end

script "pxe" do
  interpreter "bash"
  user "root"
  code <<-EOH
    mkdir /var/tftp
#rsync -av rsync://ca.archive.ubuntu.com/ubuntu/dists/precise/main/installer-amd64/current/images/netboot/ /var/tftp/
    #sed -ie "/ipv4.ip_forward/d" /etc/sysctl.conf
    echo "ipv4.ip_forward=1" > /etc/sysctl.conf
    iptables -F
    iptables -X
    iptables -t nat -F
    iptables -t nat -X
    iptables -t mangle -F
    iptables -t mangle -X
    iptables -t raw -F
    iptables -t raw -X
    iptables -A FORWARD -i eth1 -s 192.168.1.0/255.255.255.0 -j ACCEPT
    iptables -A FORWARD -i eth0 -d 192.168.1.0/255.255.255.0 -j ACCEPT
    iptables -A FORWARD -i ath0 -s 192.168.2.0/255.255.255.0 -j ACCEPT
    iptables -A FORWARD -i eth0 -d 192.168.2.0/255.255.255.0 -j ACCEPT
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
  EOH
end
