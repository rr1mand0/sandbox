# Cookbook Name:: pkmtest
# Recipe:: alpha
#
# All rights reserved.

include_recipe 'pkmtest'

cookbook_file "#{node['pkmtest']['my_dir']}/alpha_pkmtest_fancy_file.txt" do
  source "pkmtest_fancy_file.txt"
  mode 0755
  owner "root"
  group "wheel"
end
