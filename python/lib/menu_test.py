import couch
import json
import unittest
import service
import os
import sys
import logging
from datetime import datetime
from time import gmtime, strftime
from dateutil.relativedelta import relativedelta

UNITTEST_CALENDAR = 'unittest-calendar'
UNITTEST_TASK = 'unittest-meals-task'
SERVER = 'http://localhost:5984'
DBNAME = 'unittest-recipegtasktest'

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

  _recipes = [
    { 'name': 'Pasta With Boconcini',
      'ingredients': [ 'boconcini', 'pasta', 'cherry tomatoes' ]
    },
    { 'name': 'stir fry',
      'ingredients': [ 'beef', 'onions', 'red peppers' ]
    },
    { 'name': 'adobo',
      'ingredients': [ 'chicken thighs', 'soy sauce', 'vinegar', 'bay leaves', 'garlic' ]
    }

  ]

  calendarFd = None
 
  def setUp(self):
    self.calendarFd = service.GCalendar(UNITTEST_CALENDAR)
    self.assertTrue(service.GCalendarList().exists(UNITTEST_CALENDAR))

  @classmethod
  def setUpClass(cls):
    #cls.reset_events()
    pass

  @classmethod
  def reset_events(cls):
    # remove the old events
    logging.debug ("___RESET_EVENTS")
    calendarFd = service.GCalendar(UNITTEST_CALENDAR)
    events = calendarFd.delete_events(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    for meal in cls.meals:
      calendarFd.insert_event(meal)

    service.GTask(UNITTEST_TASK).clear()

    recipedb = couch.Recipes(server=SERVER, dbname=DBNAME)
    recipedb.clear()
    for recipe in cls._recipes:
      recipedb.add(recipe)


  def tearDown(self):
    pass

  @unittest.skip('')
  def test_read_events_by_period(self):
    events = self.calendarFd.get_events(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    self.assertEqual(events.__len__(), self.meals.__len__())

    new_meal = {'start':{'date': '2013-12-10'},'end':{'date': '2013-12-10'}, 'summary': 'ribs; lemon potatoes; greek salad'}
    self.calendarFd.insert_event(new_meal)

    events = self.calendarFd.get_events(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    self.assertEqual(events.__len__(), self.meals.__len__()+1)
      
  @unittest.skip('')
  def test_calendar_events_to_task(self):
    taskfd = service.GTask(UNITTEST_TASK)
    self.assertEqual(taskfd.get_items().__len__(), 0)

    self.calendarFd.push_events_to_tasks(UNITTEST_TASK, start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    self.assertNotEqual(taskfd.get_items().__len__(), 0)

  #@unittest.skip('')
  def test_shopping_list_generator(self):
    '''
    events = self.calendarFd.get_events(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')
    self.assertEqual(events.__len__(), self.meals.__len__())
    '''
    service.GTask(UNITTEST_TASK).clear()

    shoppingFd = service.ShoppingGenerator(UNITTEST_CALENDAR, UNITTEST_TASK, 
        server=SERVER, dbname=DBNAME)

    shoppingFd.publish(start_date='2013-12-01T00:00:00Z', end_date='2013-12-31T23:59:00Z')

  @unittest.skip('')
  def test_pass(self):
    self.assertTrue(True)

if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())

