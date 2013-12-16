#!/usr/bin/python
# python python/bin/caltocouch.py http://127.0.0.1:5984 Menu

import sys, getopt
import service

def main(argv):
  print ('%s' %(sys.argv))
  _service = service.GoogleService()
  _service.import_events_to_couchdb(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
   main(sys.argv[0:])



