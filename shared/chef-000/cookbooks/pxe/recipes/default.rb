
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
    notifies :restart, "script[NetworkingManager]"
end

service "dnsmasq" do
  supports :start => true, :restart => true, :status => true
end

script "NetworkingManager" do
  interpreter "bash"
  user "root"
  code <<-EOH
    restart network-manager &
  EOH
end

script "pxe" do
  interpreter "bash"
  user "root"
  code <<-EOH
    mkdir /var/tftp
    rsync -av rsync://ca.archive.ubuntu.com/ubuntu/dists/precise/main/installer-amd64/current/images/netboot/ /var/tftp/
    sed -ie "/ipv4.ip_forward/d" /etc/sysctl.conf
    echo "ipv4.ip_forward=1" >> /etc/sysctl.conf
  EOH
end
