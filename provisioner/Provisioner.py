#!/usr/bin/python
import os

class ActiveMQ(object):

class OpenVPN(object):

class Chef(object):




# Base Device class
# implements hardware 
class Device(object):
    def __init__ (self, name, type):
        self.name = name
        self.type = type

    def powerOn (self):
        print "PowerOn"

    def reboot (self):
        print "reboot"

    def set

class RtkBox(Device):
    def __init__ (self, name, isPhysical):
        self.name = name
        self.isPhysical = isPhysical
        print "RtkBox: " + self.name
    def setIsoImage(self, isoImage):

    def pxeBoot(self, preseed):

    def cdBoot(cdBoot, preseed):


class PeerNode(Device):
    def __init__ (self, name):
        self.name = name
        print "PeerNode: " + self.name

class Switch(Device):

class CiscoSwitch(Device):


# Provisioner
#   responsible for configuring all devices in the RTKNet
class Provision:
    def __init__(self, rtkbox, peerNode):
        self.rtkbox = rtkbox

    def createRtkNet(self):

    def addRtkBox(self, box):
        # add IP
      


    # write configuration to chef
    def pushToChef(self, chefhandle):


p = Provision("awn") 
p.instantiate()
