#
# Cookbook Name:: miketest
# Recipe:: default
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute
#
#

#package
package "openvpn" do
    version "2.2.1_1"
    Chef::Log.info("Package openvpn")
end

#look for data bag openvpn::test::remote_ip
bag = data_bag_item('openvpn', 'test')
ip = bag['remote_ip']
Chef::Log.info("remote_ip = #{ip}")


template "/root/mike.txt" do
	source "mike.txt.erb"
	variables ({
        :server => "chefserver.cloud.arcticwolf.biz",
        :onsy => node[:miketest][:onsy]
    })
end

Chef::Log.info("Node: #{node}")
Chef::Log.info("Role: #{node[:roles]}")

#case node[:roles]
#when "cloudconnector"
#	Chef::Log.info("My role is a cloud connector")
#when "rtkbox"
#	Chef::Log.info("My role is an RTKBox")
#else
#	Chef::Log.info("I have no idea what I am")
#end
#
Chef::Log.info("My attributes for onsy are #{node[:miketest][:onsy]}")
if node[:roles].include?('cloudconnector')
	Chef::Log.info("My role is a cloud connector")
elsif node[:roles].include?('rtkbox')
	Chef::Log.info("role is rtkbox")
else 
	Chef::Log.info("I have no idea what I am")
end
	
