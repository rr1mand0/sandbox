import unittest
import service
import os
import sys
import logging
from datetime import datetime
from time import gmtime, strftime
from dateutil.relativedelta import relativedelta

UNITTEST_CALENDAR = 'menutest-calendar'
SERVER = 'http://localhost:5984'

class GMenuTest(unittest.TestCase):
  def setUp(self):
    self.calendarListFd = service.GCalendarList()

    #if service.GCalendarList().exits(UNITTEST_CALENDAR):
    self.calendarListFd.delete(UNITTEST_CALENDAR)

    self.calendarFd = service.GCalendar(UNITTEST_CALENDAR)
    self.assertTrue(self.calendarListFd.exists(UNITTEST_CALENDAR))

  '''
  def tearDown(self):
    self.calendarListFd.delete(UNITTEST_CALENDAR)
    self.assertFalse(self.calendarListFd.exists(UNITTEST_CALENDAR))
    pass
  '''

  def test_read_events_by_period(self):
    #create events for the next week
    day = datetime.today() 
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

    for meal in meals:
      '''
      day = day + relativedelta(days=1)
      meal_event = {
        'summary': meal,
        'location': '@home',
        'start': {
          'date': day.strftime("%Y-%m-%d")
        },
        'end': {
          'date': day.strftime("%Y-%m-%d")
        },
        'attendees': [
          {
            'email': 'raymund.rimando@gmail.com',
          }
        ]
      }
      '''
      self.calendarFd.insert_event(meal)
if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())

