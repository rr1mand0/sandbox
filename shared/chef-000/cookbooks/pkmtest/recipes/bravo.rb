# Cookbook Name:: pkmtest
# Recipe:: bravo
#
# All rights reserved.

cookbook_file "#{node['pkmtest']['my_dir']}/bravo_pkmtest_fancy_file.txt" do
  source "pkmtest_fancy_file.txt"
  mode 0755
  owner "root"
  group "wheel"
end

package "vim-lite"
