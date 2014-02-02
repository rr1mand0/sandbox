#!/usr/bin/python
import argparse
import datetime
import time
import os
import logging
import service
import sys, time
import gflags

TASK     = 'GTask'
CALENDAR = 'Menu'
SERVER   = 'http://localhost:5984'
DBNAME   = 'recipes'



def do_something():
  while True:
    logging.info("Publishing")
    #SHOPPINGFD.publish(start_date='2013-12-01T00:00:00Z', 
    #  end_date='2013-12-31T23:59:00Z')
    time.sleep(30)

def run():
  with daemon.DaemonContext():
    do_something()

def process_flags(argv):
  """Uses the command-line flags to set the logging level.

  Args:
    argv: List of command line arguments passed to the python script.
  """

  # Let the gflags module process the command-line arguments.
  try:
    argv = gflags.FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\nUsage: %s ARGS\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  # Set the logging according to the command-line flag.
  #logging.getLogger().setLevel(getattr(logging, gflags.FLAGS.logging_level))


def single(args):
  service.GTask(TASK).clear()
  start_date = datetime.datetime.now()
  end_date   = start_date + one_week

  logging.info("Publishing %s-%s" % (start_date.isoformat('T'), end_date.isoformat('T')))
  SHOPPINGFD.publish(start_date='%sZ'%start_date.isoformat('T'), 
      end_date='%sZ'%end_date.isoformat('T'))

def daemon(args):
  while True:
    single(args)


if __name__ == "__main__":
  process_flags(sys.argv)
  logging.basicConfig(filename='%s/gcald.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  SHOPPINGFD = service.ShoppingGenerator(CALENDAR, TASK, server=SERVER, dbname=DBNAME)
  one_week = datetime.timedelta(days=7)

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help='sub-command help')

  parser_single = subparsers.add_parser('single', help='run as daemon')
  parser_single.set_defaults(func=single)

  args = parser.parse_args()

  args.func(args)

