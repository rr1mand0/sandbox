default['cassandra']['enable_daemon']           = true
default['cassandra']['data_dir'] = '/var/lib/cassandra'
default['cassandra']['log_dir'] = '/var/log/cassandra'
default['cassandra']['user_created_flag']  = '/usr/local/share/cassandra/conf/.user_created'

#tunable params, these are the small defaults given by the cassandra-env.sh file.
default['cassandra']['max_heap_size'] = '256M'
default['cassandra']['heap_newsize'] = '60M'
