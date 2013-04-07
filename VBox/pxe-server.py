#!/usr/bin/python

import subprocess

class VboxManager(object):
    def __init__ (self, name):
        print
        self.name = name
        #self.nic1 ("bridged")
        #self.nic2 ("intnet", "pxe")

    def modifyvm(self, args):
        cmd = ["VBoxManage modifyvm", self.name, args]
        print cmd
        p = subprocess.Popen(cmd,  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdout.readline()

    def touch(self):
        cmd = ['touch', '/tmp/xxx']
        print cmd
        print subprocess.call(cmd,  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)





mgr = VboxManager ("pxe-server-0")
#mgr.modifyvm ("--nic1 bridged")
mgr.touch()

