# Cookbook Name:: aw
# Recipe:: cassandra
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

include_recipe 'aw'

aw_root = node['aw']['root_dir']
create_inventory_cmd = "/bin/sh #{aw_root}/bin/run.sh python #{aw_root}/py/rtk/collector/setup_inventory.py update"
execute create_inventory_cmd do
  command = create_inventory_cmd
  action :run
end
