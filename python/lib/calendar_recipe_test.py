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
    self.calendarFd = service.GCalendar()

    if self.calendarListFd.exists(UNITTEST_CALENDAR):
      self.calendar = self.calendarListFd.get_calendar_by_name(UNITTEST_CALENDAR)
    else:
      self.calendar = self.calendarFd.insert(UNITTEST_CALENDAR)

    self.assertTrue(self.calendarListFd.exists(UNITTEST_CALENDAR))
  def tearDown(self):
    self.calendarListFd.delete(UNITTEST_CALENDAR)
    self.assertFalse(self.calendarListFd.exists(UNITTEST_CALENDAR))

  def test_create(self):
    self.assertTrue(True)

class ShoppingListCreator(unittest.TestCase):
  def test_create_shopping_list_from_calendar(self):
    self.assertIsNotNone({})

if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())

