import logging
import json
import unittest
import service

class ServiceTest(unittest.TestCase):
  def test_add_task(self):
    gtask = service.GoogleService().get_task_service()
    tasklist = gtask.tasklists().list().execute()
    print json.dumps(tasklist, indent=2)



if __name__ == '__main__':
  logging.basicConfig(filename='/tmp/service_test.log', level=logging.DEBUG)
  unittest.main()
