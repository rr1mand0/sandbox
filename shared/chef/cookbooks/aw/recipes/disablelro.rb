# Cookbook Name:: aw
# Recipe:: disablelro
#
# Copyright 2012, Arctic Wolf Networks
#
# All rights reserved - Do Not Redistribute

node['aw']['disablelro_interfaces'].each do |interface|
  script "install_something" do
    interpreter "bash"
    user "root"
    cwd "/tmp"
    code <<-EOH
      # Disable LRO
      rcconf=/etc/rc.conf
      interface=#{interface}
      grep -q "^ifconfig_$interface.*-lro" $rcconf
      if [ $? -ne 0 ]; then 
        sed -i .cheforig "s/^ifconfig_$interface=\\\"/ifconfig_$interface=\\\"-lro /" $rcconf
        ifconfig $interface -lro
      fi
    EOH
  end
end
