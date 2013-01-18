# Attirbutes for zabbix agent

default['zabbix']['server_hostname'] = 'monitor01.cloud.arcticwolf.biz'
default['zabbix']['server_port']     = 10051
default['zabbix']['log_path']        = '/var/log/zabbix'

default['zabbix_agent']['listen_port']            = '10050'
default['zabbix_agent']['conf_file']              = '/usr/local/etc/zabbix2/zabbix_agentd.conf'
default['zabbix_agent']['agent_name']             = node['hostname'] #default
default['zabbix_agent']['debug_level']            = '3' #4=debug, 3=warn, 2=error
default['zabbix_agent']['start_agents']           = '3'

default['zabbix_proxy']['conf_file']              = '/usr/local/etc/zabbix2/zabbix_proxy.conf'
default['zabbix_proxy']['listen_port']            = 10051
default['zabbix_proxy']['proxy_name']             = node['hostname'] #default
default['zabbix_proxy']['debug_level']            = '3' #4=debug, 3=warn, 2=error
default['zabbix_proxy']['db_path']                = '/var/db/zabbix/'
default['zabbix_proxy']['db_filename']            = 'proxy.sqlite'
default['zabbix_proxy']['start_pollers']          = '2'
default['zabbix_proxy']['start_trappers']         = '2'
default['zabbix_proxy']['start_pingers']          = '1'
default['zabbix_proxy']['start_discoverers']      = '1'
default['zabbix_proxy']['start_db_syncers']       = '2'


