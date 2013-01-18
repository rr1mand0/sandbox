#
# Cookbook Name:: pxe-server
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#
package "vim"
#package "inetutils-inetd"
#package "tftpd-hpa"
#package "dhcp3-server"
package "apache2"
package "dnsmasq"

#add pf.conf
template '/etc/default/tftpd-hpa' do
    mode "0644"
    source 'tftpd-hpa.erb'
    #notifies :restart, "service[pf]", :delayed
    variables ({
            :rootdir => "/var/lib/tftpboot"
            })
end

#template '/etc/dhcp3/dhcpd.conf' do
#mode "0644"
#source 'dhcpd.conf.erb'
#notifies :restart, "service[isc-dhcp-server])"
#end

#service "isc-dhcp-server" do
#supports :status => true, :restart => true
#action [ :enable, :start ]
#end


template '/etc/dhcp3/dhcpd.conf' do
  mode 00644
  source 'dhcpd.conf.erb'
end
 
service "isc-dhcp-server" do
  supports :restart => true, :reload => true
  action :enable
  subscribes :reload, resources("template[/etc/dhcp3/dhcpd.conf]"), :immediately
end

template '/etc/apache2/sites-available/ubuntu' do
  mode 00644
  source 'ubuntu.erb'
end
 
service "apache2" do
  supports :restart => true, :reload => true
  action :enable
  subscribes :reload, resources("template[/etc/apache2/sites-available/ubuntu"), :immediately
end


#template "/etc/nagios3/configures-nagios.conf" do
  # other parameters
#end
 
# this will fail and prevent us from restarting nagios if we broke the config
#execute "test-nagios-config" do
#command "nagios3 --verify-config"
#action :nothing
#subscribes :run, resources(:template => "/etc/nagios3/configures-nagios.conf"), :immediately
#end
