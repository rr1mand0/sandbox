#recipe for zabbix agent
include_recipe 'zabbix'

conf_file = node['zabbix_agent']['conf_file']

#TODO: differentiate between rktbox which needs to set server as proxy and other nodes
if node[:roles].include?('rtkbox')
    #set it to the remote end of the outofband tunnel
    zabbix_server = node['aw']['peernode_outofband_ip']
else
    zabbix_server = node['zabbix']['server_hostname']
end
Chef::Log.info("Setting zabbix_server to '#{zabbix_server}'")

template "#{conf_file}" do
    source "agent/zabbix_agentd.conf.erb"
    mode "0644"
    owner "root"
    group "wheel"
    variables(
        :debug_level => node['zabbix_agent']['debug_level'],
        :zabbix_server => zabbix_server,
        :listen_port  => node['zabbix_agent']['listen_port'],
        :start_agents  => node['zabbix_agent']['start_agents'],
        :agent_name  => node['zabbix_agent']['agent_name'],
        :log_path => node['zabbix']['log_path']
    )
    notifies :restart, "service[zabbix_agentd]", :delayed
end

directory "/usr/local/zabbix" do
    mode "0755"
    owner "root"
    group "wheel"
    action :create
end

template "/usr/local/zabbix/activemq_monitor.py" do
    source "agent/bin/activemq_monitor.py.erb"
    mode "0755"
    owner "root"
    group "wheel"
    variables(
        :conf_file => node['zabbix_agent']['conf_file']
    )
end
template "/usr/local/zabbix/io_stat.py" do
    source "agent/bin/io_stat.py.erb"
    mode "0755"
    owner "root"
    group "wheel"
    variables(
        :conf_file => node['zabbix_agent']['conf_file']
    )
end
template "/usr/local/zabbix/openvpn_monitor.py" do
    source "agent/bin/openvpn_monitor.py.erb"
    mode "0755"
    owner "root"
    group "wheel"
    variables(
        :conf_file => node['zabbix_agent']['conf_file']
    )
end


template "/etc/rc.conf.d/zabbix_agentd" do
    source "agent/rc.conf.d/zabbix_agentd.erb"
    mode "0644"
    owner "root"
    group "wheel"
end

#add cron entries:
#* * * * * /usr/local/zabbix/io_stat.py >/tmp/io_stat.log 2>&1
#* * * * * /usr/local/zabbix/activemq_monitor.py brokers >/tmp/activemq_broker.log 2>&1
#* * * * * /usr/local/zabbix/activemq_monitor.py destinations >/tmp/activemq_destinations.log 2>&1
cron "io_stat" do
    command "/usr/local/zabbix/io_stat.py >/tmp/io_stat.log 2>&1"    
    user "zabbix"
end
cron "activemq_monitor_brokers" do
    command "/usr/local/zabbix/activemq_monitor.py brokers >/tmp/activemq_broker.log 2>&1"
    user "zabbix"
end
cron "activemq_monitor_queues" do
    command "/usr/local/zabbix/activemq_monitor.py destinations >/tmp/activemq_destinations.log 2>&1"
    user "zabbix"
end
cron "openvpn_outofband" do
    command "/usr/local/zabbix/openvpn_monitor.py 1150 outofband >/tmp/openvpn_outofband.log 2>&1"
    user "zabbix"
end
cron "openvpn_inband" do
    command "/usr/local/zabbix/openvpn_monitor.py 1151 inband >/tmp/openvpn_inband.log 2>&1"
    user "zabbix"
end


service "zabbix_agentd" do
        supports :start => true, :restart => true, :status => true
        action :start
end
