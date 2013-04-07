#!/usr/bin/python

import os
import argparse

class TemplateBuilder(object):
    def __init__ (self, iso, preseed):
        print ("Template")

    def install_chef(self):
        print

    def cleanup (self):
        print
        # delete udev rules

    def createBase(self, output):
        print

    def generateAlphaBravo(self, output):
        print ("generateAlphaBravo")
        # configure
        # boot
        # cleanup
        # pack-up


class Physical(TemplateBuilder):
    def __init__ (self, iso, preseed):
        print ("Physical")

    def setup_pxe(self):
        print ("PXE config")

class Vagrant(TemplateBuilder):
    def __init__ (self, iso, preseed):
        print ("Vagrant")
        self.iso = iso
        self.preseed = preseed

    def unpack_iso(self):
        print ("unpack_iso")


class OpenStack(TemplateBuilder):
    def __init__ (self):
        print ("OpenStack")

parser = argparse.ArgumentParser (description = 'Box creator')
parser.add_argument ('--iso', dest='dest', action='store_const',
            help='set the ISO disk to boot from')

box = Physical("iso.img", "preseed.cfg")
box.generateAlphaBravo("alpha.box")


args = parser.parse_args()
print (args.accumulate(args.integer))
