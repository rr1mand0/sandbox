maintainer       "Arctic Wolf Networks"
maintainer_email "michael.hart@arcticwolf.com"
license          "All rights reserved"
description      "Installs/Configures zabbix"
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          "0.1.4"
recipe           "default", "Installs Zabbix"
recipe           "agent", "Installs Zabbix Agent"
recipe           "proxy", "Installs Zabbix Proxy"
