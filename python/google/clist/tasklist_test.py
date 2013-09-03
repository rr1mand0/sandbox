from googleservice import GoogleService
from tasklist import TaskList
from calendar  import CalendarList
from tasks import Task
from oauth2client.client import AccessTokenRefreshError
import sys
import gflags
import unittest
import json

"""
import logging
FLAGS = gflags.FLAGS
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')
"""


class TaskListTest(unittest.TestCase):
  def setUp(self):
    self.calendar_service = GoogleService().get_calendar_service()
    self.task_service     = GoogleService().get_task_service()
    self.tl               = self.task_service.tasklists()
    self.task             = self.task_service.tasks()
    #print json.dumps(self.tl.list().execute(), indent=2)

  def testcreate(self):
    tasklist = TaskList("rays-test=01")
    tasklist.create()
    self.failIf(not tasklist.exists())

  #@unittest.skip("demonstrating skipping")
  def testcreate_and_delete(self):
    tasklist = TaskList("rays-test=00")
    tasklist.create()
    self.failIf(not tasklist.exists())

    tasklist.delete()
    self.failIf(tasklist.exists())

  """ add task to a tasklist """
  #@unittest.skip("demonstrating skipping")
  def test_add_tasks_to_tasklist(self):
    #print ("adding tasks")
    tasklist = TaskList("task-inserter")
    tasklist.create()
    self.failIf(not tasklist.exists())

    tl_id = tasklist.get_id()
    task = Task(self.task, tl_id)
    task.create()

  #@unittest.skip("demonstrating skipping")
  def test_calandar_list(self):
    calendar = CalendarList(self.calendar_service, "Menu")
    self.failIf(not calendar.exists())


def main(argv):
  suite = unittest.TestLoader().loadTestsFromTestCase(TaskListTest)
  unittest.TextTestRunner(verbosity=2).run(suite)
  #unittest.main()

if __name__ == '__main__':
  main(sys.argv)
