Description
===========

Configures ActiveMQ. The ActiveMQ 5.5.0 package is inherently broken so we do a few things:
 * remove broken link to data and set data to /var/activemq (where the actual queue's live)
 * java tuning is in /etc/rc.conf.d/activemq
 * clean out all the sample configs and put in place only what's required.

TODO:
 * set remote broker name on the peernode config to configurable
 * configurable java tuning params
 * tunable configs for activemq
 * security for activemq
   * basic authentication is already setup. Secure this.
   * ssl from external

Requirements
============

ActiveMQ 5.5.0 package installed

Attributes
==========

Usage
=====

