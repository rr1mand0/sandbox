maintainer       "Arctic Wolf Networks"
maintainer_email "michael.hart@arcticwolf.com"
license          "All rights reserved"
description      "Installs/Configures openvpn and pf for AW"
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          "0.4.2"
depends          'aw'
recipe           "openvpn", "Base AW OpenVPN configuration."
recipe           "openvpn::peernode", "Configures OpenVPN node to act as a peer node."
recipe           "openvpn::rtkbox", "Configures OpenVPN node to act as an rtkbox."
