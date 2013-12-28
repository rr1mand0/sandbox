import daemon
import time
import os
import logging
import service
import sys, time

TASK     = 'GTask'
CALENDAR = 'GMenu'
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

import datetime

if __name__ == "__main__":
  logging.basicConfig(filename='%s/gcald.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  SHOPPINGFD = service.ShoppingGenerator(CALENDAR, TASK, server=SERVER, dbname=DBNAME)
  one_week = datetime.timedelta(days=7)
  #for loop in range(1,2):
  while True:
    service.GTask(TASK).clear()
    start_date = datetime.datetime.now()
    end_date   = start_date + one_week


    logging.info("Publishing %s-%s" % (start_date.isoformat('T'), end_date.isoformat('T')))
    SHOPPINGFD.publish(start_date='%sZ'%start_date.isoformat('T'), 
        end_date='%sZ'%end_date.isoformat('T'))
    time.sleep(60)

