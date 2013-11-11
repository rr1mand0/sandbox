#!/usr/bin/python

import sys, getopt
import service

def main(argv):
  print ('%s' %(sys.argv))
  _service = service.GoogleService()
  _service.import_events_to_couchdb(sys.argv[2])

if __name__ == "__main__":
   main(sys.argv[0:])



