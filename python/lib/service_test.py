import sys
import os
import couch
import logging
import json
import unittest
import service
UNITTEST_TASK = 'unittest-task'
UNITTEST_CALENDAR = 'unittest-calendar'
SERVER = 'http://localhost:5984'
DBNAME = 'recipegtasktest'

class GCalendarTest(unittest.TestCase):
  def test_create_calendar(self):
    self.calendarListFd = service.GCalendarList()
    if self.calendarListFd.exists(UNITTEST_CALENDAR):
      self.calendar = self.calendarListFd.get_calendar_by_name(UNITTEST_CALENDAR)
    else:
      self.calendar = self.calendarListFd.create(UNITTEST_CALENDAR)

    self.assertTrue(self.calendarListFd.exists(UNITTEST_CALENDAR))

class RecipeGTaskTest(unittest.TestCase):
  def test_couch_to_gtask(self):
    self.recipedb = couch.Recipes(server=SERVER, dbname=DBNAME)
    self.boconcini = {
      "name": "Pasta With Boconcini",
      "ingredients": [
        "boconcini",
        "pasta",
        "cherry tomatoes"
      ]
    }
    self.tasklistfd = service.GTaskList()
    self.tasklist = self.tasklistfd.get_list_by_name(UNITTEST_TASK)

class GTaskTest(unittest.TestCase):
  new_tasklist = {
    'title': UNITTEST_TASK
  }

  def setUp(self):
    self.tasklistfd = service.GTaskList()
    if self.tasklistfd.exists(UNITTEST_TASK):
      self.tasklist = self.tasklistfd.get_list_by_name(UNITTEST_TASK)
    else:
      self.tasklist = self.tasklistfd.create(self.new_tasklist)
    self.assertTrue(self.tasklistfd.exists(UNITTEST_TASK))

  
  def tearDown(self):
    self.tasklistfd.delete(self.new_tasklist['title'])
    self.assertFalse(self.tasklistfd.exists(UNITTEST_TASK))
    pass

  def test_one(self):
    pass

  #@unittest.skip('wip')
  def test_add_task(self):
    taskfd = service.GTask(id = self.tasklist['id'])
    task_len =  taskfd.__len__()
    maxval = 10
    for i in range(0, maxval):
      # insert a new task
      newtask = {
        'title': 'check me %d' % i
      }
      taskfd.insert(newtask)

      # make sure we found it
      task = taskfd.get_by_title(newtask['title'])
      self.assertIsNotNone(task)

      # now delete it
      taskfd.delete_by_title(newtask['title'])
      self.assertEquals(task_len,  taskfd.__len__())
    
  def test_list_tasks(self):
    taskfd = service.GTask(id = self.tasklist['id'])
    self.assertIsNotNone(taskfd.list())


  @unittest.skip ('')
  def test_pass(self):
    self.assertTrue(True)



if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())
  #suite = unittest.TestLoader().loadTestsFromTestCase(GCalendarTest)
  #sys.exit(unittest.TextTestRunner(verbosity=2).run(suite))
  
