import sys
from time import gmtime, strftime
import service
import unittest
import logging
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

UNITTEST_CALENDAR = 'unittest-calendar'
SERVER = 'http://localhost:5984'

class GCalendarTest(unittest.TestCase):
  def setUp(self):
    self.calendarListFd = service.GCalendarList()
    self.calendarFd = service.GCalendar(UNITTEST_CALENDAR)
    self.assertTrue(self.calendarListFd.exists(UNITTEST_CALENDAR))

  def tearDown(self):
    self.calendarListFd.delete(UNITTEST_CALENDAR)
    self.assertFalse(self.calendarListFd.exists(UNITTEST_CALENDAR))
    pass

  def test_existing_calendar(self):
    self.assertIsNotNone(service.GCalendarList().exists("Menu"))


  def test_create_event(self):
    all_day_event = {
      'summary': 'New Appointment',
      'location': 'Somewhere',
      'start': {
        'date': strftime("%Y-%m-%d", gmtime())
        #'dateTime': strftime("%Y-%m-%d %H:%M:%S", gmtime())
      },
      'end': {
        'date': strftime("%Y-%m-%d", gmtime())
        #'dateTime': strftime("%Y-%m-%d %H:%M:%S", gmtime())
      },
      'attendees': [
        {
          'email': 'raymund.rimando@gmail.com',
        }
      ]
    }
    event = {
      'summary': 'New Appointment',
      'location': 'Somewhere',
      'start': {
        'dateTime': strftime("%Y-%m-%d %H:%M:%S", gmtime())
      },
      'end': {
        'dateTime': strftime("%Y-%m-%d %H:%M:%S", gmtime())
      },
      'attendees': [
        {
          'email': 'raymund.rimando@gmail.com',
        }
      ]
    }
    
    self.calendarFd.insert_event(all_day_event)
    #eventFd = service.GEvents()
    self.assertTrue(True)

class ShoppingListCreator(unittest.TestCase):
  def test_create_shopping_list_from_calendar(self):
    self.assertIsNotNone({})

if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())

