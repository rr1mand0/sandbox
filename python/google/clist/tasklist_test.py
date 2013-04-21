from googleservice import GoogleService
from tasklist import TaskList
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
    self.service = GoogleService().get_service()
    self.tl = self.service.tasklists()
    self.task = self.service.tasks()
    #print json.dumps(self.tl.list().execute(), indent=2)

  def testcreate_and_delete(self):
    tasklist = TaskList(self.tl, "rays-test=00")
    tasklist.insert()
    self.failIf(not tasklist.exists())

    tasklist.delete()
    self.failIf(tasklist.exists())

  def test_add_tasks_to_tasklist(self):
    print ("adding tasks")
    tasklist = TaskList(self.tl, "task-inserter")
    tasklist.insert()
    self.failIf(not tasklist.exists())

    tl_id = tasklist.get_id()
    task = Task(self.task, tl_id)
    task.insert()

    pass


def main(argv):
  unittest.main()

if __name__ == '__main__':
  main(sys.argv)
