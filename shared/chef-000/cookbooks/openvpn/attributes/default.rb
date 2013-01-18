# Attirbutes for openvpn / AW networking

default['openvpn']['inband_enable']        = true
default['openvpn']['outofband_enable']     = true

default['openvpn']['conf_dir']             = '/usr/local/etc/openvpn'
default['openvpn']['rc_dir']               = '/usr/local/etc/rc.d'
default['openvpn']['inband_port']          = 1194
default['openvpn']['outofband_port']       = 4463
default['openvpn']['inband_mgmt_port']     = 1151
default['openvpn']['outofband_mgmt_port']  = 1150

default['pf']['conf_dir']                  = '/etc'
