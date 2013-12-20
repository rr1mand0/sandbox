import logging
import json
import unittest
import service
NEW_TASKLIST = 'unittest'


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
    self.tasklist = self.tasklistfd.get_list_by_name(NEW_TASKLIST)

class GTaskTest(unittest.TestCase):
  new_tasklist = {
    'title': NEW_TASKLIST
  }

  def setUp(self):
    self.tasklistfd = service.GTaskList()
    if self.tasklistfd.exists(NEW_TASKLIST):
      self.tasklist = self.tasklistfd.get_list_by_name(NEW_TASKLIST)
    else:
      self.tasklist = self.tasklistfd.create(self.new_tasklist)
    self.assertTrue(self.tasklistfd.exists(NEW_TASKLIST))

  
  def tearDown(self):
    #self.tasklistfd.delete(self.new_tasklist['title'])
    #self.assertFalse(self.tasklistfd.exists(NEW_TASKLIST))
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
      print 'inserting: %s' % newtask['title']
      taskfd.insert(newtask)

      # make sure we found it
      #task = taskfd.get_by_title(newtask['title'])
      #self.assertEquals(task, {})

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
  logging.basicConfig(filename='/tmp/service_test.log', level=logging.INFO)
  unittest.main()
