# Attirbutes for AW recipes

# Peernode IP, must be set (as node attribute)
default['aw']['peernode_public_ip']     = nil

# list of services to install for AW package,
#   this should be specified as attributes on a role or the node (eg: peernode, rtkbox)
default['aw']['services']               = [ ]

# The packages server, or nil to use the package published with the cookbook
default['aw']['packages_url']           = 'https://packages.cloud.arcticwolf.biz'

# Will look for package under <packages_url>/<packages_category>
#   (Ignored if packages_url is nil)
#   ci : Uploaded by Jenkins whenever a CI build completes successfully.
#   dev : For unregulated use by development.
#   release : production versions
default['aw']['packages_category']      = 'ci'

# A specific version or nil to indicate 'the latest published version',
#   ignored if packages_url is nil
default['aw']['package_version']        = nil
default['aw']['package_name']           = 'aw'

# true: will perform upgrade if a newer version exists
default['aw']['enable_upgrade']         = false

# true: always perform the install even if the package is the same or older
#   than the installed version. Ignored if 'enable_upgarde' is false
default['aw']['always_upgrade']         = false

# Only list packages that aren't part of the base template
default['aw']['dependency_packages']    = [
]

# Only list pips that aren't part of the base template
default['aw']['dependency_pips']        = [
  'stompest',
  'ipaddr',
  'web.py'
]

default['aw']['root_dir']               = '/usr/local/aw'
default['aw']['etc_dir']                = '/usr/local/aw/etc'
default['aw']['log_dir']                = '/usr/local/aw/log'
default['aw']['rc.d_dir']               = '/usr/local/etc/rc.d'
default['aw']['rc.conf.d_dir']          = '/etc/rc.conf.d'

default['aw']['peernode_inband_ip']     = '10.8.3.3'
default['aw']['peernode_outofband_ip']  = '10.8.1.3'

default['aw']['rtkbox_inband_ip']       = '10.8.3.10'
default['aw']['rtkbox_outofband_ip']    = '10.8.1.10'

default['aw']['devtools']               = [ 'rsync', 'vim-lite' ]

default['aw']['devloopback_ips']        = [ '10.8.9.33', '10.8.9.44', '10.8.9.55' ]

default['aw']['awdivert_enable']        = true

default['aw']['rtkwlf_uid']             = 8639
default['aw']['rtkwlf_gid']             = 8639
default['aw']['rtkwlf_shell']           = '/bin/sh'

default['aw']['package_cache']          = '/var/cache/aw/aw.tbz'

default['aw']['peernode_external_interface'] = 'xn0'

default['aw']['disablelro_interfaces']  = [ 'xn0', 'xn1' ]

default['aw']['rtkbox_bridge_interface']    = 'bridge0'
default['aw']['rtkbox_bridged_interfaces']  = [ 'em2', 'em3' ]

# FIXME - this should be auto-determined
default['aw']['rtkbox_bridge_ip']       = '10.8.7.10' # This should be overridden

default['aw']['inband_interface']       = 'tap3'
default['aw']['outofband_interface']    = 'tun1'

default['sudo']['sudoers_file']         = '/usr/local/etc/sudoers'
default['sudo']['sudowheel_enable']     = true
