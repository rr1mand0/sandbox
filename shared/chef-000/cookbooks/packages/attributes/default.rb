# Attirbutes for AW recipes

# These are NOT installed by this recipe
default['packages']['ssl_cert']           = '/etc/ssl/certs/packages.cloud.arcticwolf.biz.cert.pem'
default['packages']['ssl_key']            = '/etc/ssl/private/packages.cloud.arcticwolf.biz.key.pem'
default['packages']['ssl_ca_cert']        = '/etc/ssl/certs/cloud.arcticwolf.biz-CA.cert.pem'

# This will need to be updated if moved to a different host
default['packages']['server_name']        = 'packages.cloud.arcticwolf.biz'

default['packages']['packages_root']      = '/var/aw-packages'
default['packages']['package_categories'] = [ 'ci', 'dev', 'release' ]
default['packages']['read_port']          = 443
default['packages']['write_port']         = 444
default['packages']['read_user']          = '^Packaging'
default['packages']['write_user']         = '^Packaging Creator'
