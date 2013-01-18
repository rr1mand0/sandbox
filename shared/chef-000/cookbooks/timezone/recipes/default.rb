#
# Cookbook Name:: timezone
# Recipe:: default
#
# Copyright 2013, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute
#

zone = node['timezone']['zone']
timezonefile = "/usr/share/zoneinfo/#{zone}"
localtimefile = "/etc/localtime"

execute "settimezone" do
    #if the localtimefile doesn't exist or point at the timezone file, remove it and link it.
    command "if [ ! #{localtimefile} -ef #{timezonefile} ]; then if [ -e #{localtimefile} ]; then rm #{localtimefile}; fi; ln -s #{timezonefile} #{localtimefile}; fi"
end

