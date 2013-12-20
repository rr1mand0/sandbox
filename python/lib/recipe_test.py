import os
import service
import json
import couch
import logging
import unittest

SERVER = 'http://localhost:5984'
DBNAME = 'test-recipe'

class RecipeTest(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    super(RecipeTest, cls).setUpClass()
    recipedb = couch.Recipes(server=SERVER, dbname=DBNAME)

  @classmethod
  def tearDownClass(cls):
    super(RecipeTest, cls).tearDownClass()
    recipedb = couch.Recipes(server=SERVER, dbname=DBNAME)
    recipedb.destroy()

  def setUp(self):
    self.recipedb = couch.Recipes(server=SERVER, dbname=DBNAME)
    self.boconcini = {
      "name": "Pasta With Boconcini",
      "ingredients": [
        "boconcini",
        "pasta",
        "cherry tomatoes"
      ]
    }
    self.recipedb.add(self.boconcini)

  def tearDown(self):
    self.recipedb.delete(self.boconcini['name'])
    self.assertEquals(self.recipedb.__len__(), 0)


  def test_create_by_args(self):
    recipe_count = self.recipedb.__len__()
    self.recipedb.add_with_ingredients ('adobo', 
      ingredients = "chicken thighs, soy sauce, vinegar, bay leaves, peppercorn")
    self.assertEquals(self.recipedb.exists('adobo'), True)
    self.assertEquals(self.recipedb.__len__(), recipe_count+1)

    self.recipedb.delete('adobo')
    self.assertEquals(self.recipedb.exists('adobo'), False)
    self.assertEquals(self.recipedb.__len__(), recipe_count)


  def test_create(self):
    self.assertEquals(self.recipedb.exists(self.boconcini['name']), True)
    self.assertEquals(self.recipedb.__len__(), 1)


  def test_show(self):
    doc = self.recipedb.get_doc(self.boconcini['name'])
    self.assertIsNotNone(doc)
    self.assertEqual(doc, self.boconcini)

  #@unittest.skip('none')
  def test_modify(self):
    new_ingredients = ['tomatoes', 'garlic', 'peppercorn']
    recipe_count = self.recipedb.__len__()
    ingredient_count = self.boconcini['ingredients'].__len__()

    for ingredient in new_ingredients:
      self.boconcini['ingredients'].append(ingredient)
      ingredient_count = ingredient_count + 1
      self.assertEquals(self.boconcini['ingredients'].__len__(), ingredient_count)

      self.recipedb.add(self.boconcini)
      self.assertEquals(self.recipedb.__len__(), recipe_count)

      doc = self.recipedb.get_doc(self.boconcini['name'])
      self.assertEqual(doc['ingredients'].__len__(), self.boconcini['ingredients'].__len__())

  def test_export_to_gtask(self):
    unitest_tasklist_name = 'unittest'
    tasklist = service.GTaskList().get_list_by_name(unitest_tasklist_name)
    taskfd = service.GTask(id = tasklist['id'])

    task_len =  taskfd.__len__()
    self.recipedb.export_to_gtask(self.boconcini['name'], unitest_tasklist_name)
    self.assertEquals(task_len + self.boconcini['ingredients'].__len__(),  taskfd.__len__())

  @unittest.skip('none')
  def test_list(self):
    pass

  @unittest.skip('none')
  def test_delete(self):
    pass

  def test_to_tasks(self):
    pass



if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.INFO)
  unittest.main()
