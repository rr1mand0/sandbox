#recipe for zabbix proxy
include_recipe 'zabbix'

conf_file = node['zabbix_proxy']['conf_file']

db_path = node['zabbix_proxy']['db_path']
directory "#{db_path}" do
    mode "0755"
    owner "zabbix"
    group "zabbix"
    action :create
end

template "#{conf_file}" do
    source "proxy/zabbix_proxy.conf.erb"
    mode "0644"
    owner "root"
    group "wheel"
    notifies :restart, "service[zabbix_proxy]", :delayed
    variables(
        :zabbix_server => node['zabbix']['server_hostname'],
        :zabbix_server_port => node['zabbix']['server_port'],
        :proxy_name  => node['zabbix_proxy']['proxy_name'],
        :listen_port  => node['zabbix_proxy']['listen_port'],
        :log_path  => node['zabbix']['log_path'],
        :debug_level => node['zabbix_proxy']['debug_level'],
        :db_path => node['zabbix_proxy']['db_path'],
        :db_filename => node['zabbix_proxy']['db_filename'],
        :start_pollers => node['zabbix_proxy']['start_pollers'],
        :start_trappers => node['zabbix_proxy']['start_trappers'],
        :start_pingers => node['zabbix_proxy']['start_pingers'],
        :start_discoverers => node['zabbix_proxy']['start_discoverers'],
        :start_db_syncers => node['zabbix_proxy']['start_db_syncers']
    )
end

template "/etc/rc.conf.d/zabbix_proxy" do
    source "proxy/rc.conf.d/zabbix_proxy.erb"
    mode "0644"
    owner "root"
    group "wheel"
end

service "zabbix_proxy" do
        supports :start => true, :restart => true, :status => true
        action :start
end
