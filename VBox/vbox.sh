#!/usr/bin/python

import os

class VBoxManage:
    def __init__ (self, program = "/usr/bin/VBoxManage", vm=None):
        self.program = program
        self.vm = vm

    def createVM (self, vm):
        returner = True
        self.vm = vm
