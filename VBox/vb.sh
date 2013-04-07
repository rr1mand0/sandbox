#!/usr/bin/python
import os
import time

class NICTYPE:
    Disabled, NAT, Bridge, IntNet, Host = range(5)


class NAT:
    def __init__(self, name, type, src_ip, src_port, dest_ip, dest_port):
        self.name = name
        self.type = type
        self.src_ip = src_ip
        self.src_port = src_port
        self.dest_ip = dest_ip
        self.dest_port = port
    
class NIC(object):
    def __init__(self, type, name=None):
        self.type = None
        self.name = name

    def configure(self, name, index):
        pass

class BridgeNic(NIC):
    def __init__(self, name=None):
        self.type = NICTYPE.Bridge
        self.name = name

    def configure (self, name, index):
        return self.call("VBoxManage modifyvm --nic" + index + " " + self.type)


class Command(object):
    def call(self, command):
        print(command)
        rc = os.system(command + " &>/dev/null")
        return 0 if rc else 1


class Vbox(Command):
    def __init__(self, name, ostype='Ubuntu_64'):
        self.nicIndex = 1
        self.name = name
        self.ostype = ostype
        if not self.exists():
            self.call("VBoxManage createvm --name " + self.name + " --ostype Debian --register")

    def display(self):
        print "name = " + self.name + "; ostype = "+ self.ostype

    def exists (self):
        return self.call("VBoxManage list vms|grep " + self.name)

    def delete(self):
        return self.call("VBoxManage unregistervm --delete " + self.name)

    def addHD(self, hd):
        pass

    def memory(self, ram):
        return self.call("VBoxManage modifyvm " + self.name + " --memory " + ram)

    def isoBoot(self, iso):
        pass

    def installVBox(self):
        pass

    def powerOff(self):
        pass

    def createVagrantBox(self, box):
        pass

    def addNic(self, nic):
        return nic.configure(self.name, self.nicIndex)



box = Vbox(name="testmachine")
box.addHD("2G")
box.memory("512M")
box.isoBoot("~/Downloads/ubuntu-12.04-server-amd64.iso")

bridgeNic = NIC (NICTYPE.Bridge, name="en0")
box.addNic(bridgeNic)

natNic = NIC(NICTYPE.NAT)
box.installVBox()

box.powerOff()

box.createVagrantBox("vagrant.box")

box.display()
time.sleep(10)
box.delete()
