import unittest
import service
import os
import sys
import logging
from datetime import datetime
from time import gmtime, strftime
from dateutil.relativedelta import relativedelta

UNITTEST_CALENDAR = 'Meds'
SERVER = 'http://localhost:5984'

class GMenuTest(unittest.TestCase):
  meals = [
    {'start':{'date': '2013-12-01'},'end':{'date': '2013-12-01'}, 'summary': 'adobo'}, 
    {'start':{'date': '2013-12-02'},'end':{'date': '2013-12-02'}, 'summary': 'pasta with boconcini'}, 
    {'start':{'date': '2013-12-03'},'end':{'date': '2013-12-03'}, 'summary': 'stir fry; rice'},
    {'start':{'date': '2013-12-04'},'end':{'date': '2013-12-04'}, 'summary': 'chicken stew'},
    {'start':{'date': '2013-12-05'},'end':{'date': '2013-12-05'}, 'summary': 'basil salmon; rice; cuccumber salad'},
    {'start':{'date': '2013-12-06'},'end':{'date': '2013-12-06'}, 'summary': 'burgers; french fries'},
    {'start':{'date': '2013-12-07'},'end':{'date': '2013-12-07'}, 'summary': 'paella'},
    {'start':{'date': '2013-12-08'},'end':{'date': '2013-12-08'}, 'summary': 'chicken cacciatore; rice'},
    {'start':{'date': '2013-12-09'},'end':{'date': '2013-12-09'}, 'summary': 'rib eye; mashed potatoes; green beans'}
  ]

  def setUp(self):
    self.calendarListFd = service.GCalendarList()
    #self.calendarListFd.delete(UNITTEST_CALENDAR)

    if not self.calendarListFd.exists(UNITTEST_CALENDAR):
      self.calendarFd = service.GCalendar(UNITTEST_CALENDAR)
      self.assertTrue(self.calendarListFd.exists(UNITTEST_CALENDAR))

    else:
      self.calendarFd = service.GCalendar(UNITTEST_CALENDAR)

    self.reset_events()

  def reset_events(self):
    # remove the old events
    events = self.calendarFd.delete_events(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    for meal in self.meals:
      self.calendarFd.insert_event(meal)

  def tearDown(self):
    pass

  def test_read_events_by_period(self):
    events = self.calendarFd.get_events(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    self.assertEqual(events.__len__(), self.meals.__len__())

    new_meal = {'start':{'date': '2013-12-10'},'end':{'date': '2013-12-10'}, 'summary': 'ribs; lemon potatoes; greek salad'}
    self.calendarFd.insert_event(new_meal)

    events = self.calendarFd.get_events(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    self.assertEqual(events.__len__(), self.meals.__len__()+1)
      
if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())

