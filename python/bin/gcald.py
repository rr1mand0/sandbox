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
  end_date   = start_date + datetime.timedelta(days=args.duration)

  logging.info("Publishing %s-%s" % (start_date.isoformat('T'), end_date.isoformat('T')))
  SHOPPINGFD.publish(start_date='%sZ'%start_date.isoformat('T'), 
      end_date='%sZ'%end_date.isoformat('T'))

def daemon(args):
  while True:
    single(args)


if __name__ == "__main__":
  #process_flags(sys.argv)
  logging.basicConfig(filename='%s/gcald.log' % os.environ['LOG_DIR'], level=logging.DEBUG)

  #parser = argparse.ArgumentParser()
  #parser.add_argument('duration', help='days to dump')

  #parser_single subparsers.add_parser('single', help='run as daemon')
  #parser_single.set_defaults(func=single)

  #args = parser.parse_args()


  #single(args)
  parser = argparse.ArgumentParser()
  parser.add_argument("--duration", help="days to dump", default=7, type=int)
  parser.add_argument("--calendar", help="calendar to sync from", default=CALENDAR)
  parser.add_argument("--task",     help="task list to sync to",  default=TASK)
  parser.add_argument("--dbname",   help="couchdb to read from",  default=DBNAME)
  parser.add_argument("--server",   help="couchdb server url",    default=SERVER)
  args = parser.parse_args()

  SHOPPINGFD = service.ShoppingGenerator(args.calendar, args.task, server=args.server, dbname=args.dbname)
  single(args)
