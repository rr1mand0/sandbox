import logging
import json
import unittest
import service
NEW_TASKLIST = 'test-new-tasklist'


class GTaskTest(unittest.TestCase):
  new_tasklist = {
    'title': NEW_TASKLIST
  }

  def setUp(self):
    self.tasklistfd = service.GTaskList()
    self.tasklist = self.tasklistfd.tasklist_create(self.new_tasklist)
    print self.tasklist
    self.assertTrue(self.tasklistfd.tasklist_exists(NEW_TASKLIST))

  
  #def tearDown(self):
  #  self.tasklist.tasklist_delete(self.new_tasklist['title'])
  #  self.assertFalse(self.tasklist.tasklist_exists(NEW_TASKLIST))

  def test_one(self):
    pass

  #@unittest.skip('wip')
  def test_add_task(self):
    task = {
      'title': 'check me'
    }

    # add tasks to tasklist
    id = self.tasklist['id']
    print ('id: %s' % id)
    self.task = service.GTask(id = id)
    #self.task.insert(task)
    
    #print json.dumps(tasklist, indent=2)

  @unittest.skip ('')
  def test_pass(self):
    self.assertTrue(True)



if __name__ == '__main__':
  logging.basicConfig(filename='/tmp/service_test.log', level=logging.INFO)
  unittest.main()
