Description
===========
Configures and starts OpenVPN and associated pf and routes for AWN on both the RTKBox and the PeerNode

Two roles are used:
 * 'peernode' - node is the cloud connector, essentially the vpn concentrator or server.
 * 'rtkbox' - node is the rtkbox, or the vpn client

Requirements
============
Requires:
 * OpenVPN 2.2.1 (not explicitly defined)
 * FreeBSD (not explicitly defined)

Attributes
==========
See attributes/default.rb

Routes
------

This applies to the PeerNode only. Because we need to route traffic from the Internet back to the customer networks, there is a separate config file to handle this case. The routes themselves are stored in /usr/local/etc/openvpn/routes.txt in the format of "network gateway", one per line. For example:

    10.8.7.0/24 10.8.3.10
    10.8.8.0/24 10.8.3.10

From the config, each item in "customer\_networks" is translated into a line in this file, with `rtkbox_inband_ip` being the gateway. The routes.txt file should not be editted directly, as chef overwites it.  Instead the data bag should be editted, and then either wait for chef to run as scheduled or run "chef-client" on the node directly.

These routes are inserted by specifying the "up /usr/local/etc/openvpn/vpn\_up.sh" stanza in openvpn\_inband.conf, which means openvpn will run the script (or fail to start) when it brings the tunnel up. That script simply loops over the routes in the file and starts them.

Packet Filter
-------------

The openvpn service also enables/disables the 'pf' packetfilter, using rules in /etc/pf.conf, which are also managed in this cookbook.
 
Usage
=====

 * Replaces the default /usr/local/etc/rc.d/openvpn to add in route logic. 
 * Installs the keys
 * Setups up two tunnel services, openvpn\_inband and openvpn\_outofband and starts them.
 * To start the service "service openvpn\_inband start" and "service openvpn\_outofband start". 
 
Todo
====

On the TODO list:
 * Sort out the keys. Today we're handing out a static key
 * Make more of the vpn connection stuff configurable by customer. Too much is hard coded, no way to tune it.
