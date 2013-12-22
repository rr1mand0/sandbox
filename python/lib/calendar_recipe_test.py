import sys
import service
import unittest
import logging
import os

UNITTEST_CALENDAR = 'unittest-calendar'
SERVER = 'http://localhost:5984'

class GCalendarTest(unittest.TestCase):
  def setUp(self):
    self.calendarListFd = service.GCalendarList()

    if self.calendarListFd.exists(UNITTEST_CALENDAR):
      self.calendar = self.calendarListFd.get_calendar_by_name(UNITTEST_CALENDAR)
    else:
      self.calendarFd = service.GCalendar(UNITTEST_CALENDAR)

    self.assertTrue(self.calendarListFd.exists(UNITTEST_CALENDAR))
  def tearDown(self):
    self.calendarListFd.delete(UNITTEST_CALENDAR)
    self.assertFalse(self.calendarListFd.exists(UNITTEST_CALENDAR))

  def test_create_event(self):
    event = {
      'summary': 'Appointment',
      'location': 'Somewhere',
      'start': {
        'dateTime': '2011-06-03T10:00:00.000-07:00'
      },
      'end': {
        'dateTime': '2011-06-03T10:25:00.000-07:00'
      },
      'attendees': [
        {
          'email': 'raymund.rimando@gmail.com',
        }
      ]
    }
    
    self.calendarFd.insert_event(event)
    #eventFd = service.GEvents()
    self.assertTrue(True)

class ShoppingListCreator(unittest.TestCase):
  def test_create_shopping_list_from_calendar(self):
    self.assertIsNotNone({})

if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())

