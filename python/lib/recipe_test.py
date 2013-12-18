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


  def test_create(self):
    self.assertEquals(self.recipedb.exists(self.boconcini['name']), True)
    self.assertEquals(self.recipedb.__len__(), 1)


  def test_show(self):
    doc = self.recipedb.get_doc(self.boconcini['name'])
    self.assertIsNotNone(doc)
    self.assertEqual(doc, self.boconcini)

  #@unittest.skip('none')
  def test_modify(self):
    self.boconcini['ingredients'].append('salt')
    self.recipedb.update(self.boconcini)

    doc = self.recipedb.get_doc(self.boconcini['name'])
    self.assertEqual(doc['ingredients'].__len__(), self.boconcini['ingredients'].__len__())

  @unittest.skip('none')
  def test_list(self):
    pass

  @unittest.skip('none')
  def test_delete(self):
    pass




if __name__ == '__main__':
  logging.basicConfig(filename='/tmp/recipe.log', level=logging.DEBUG)
  #logging.basicConfig(level=logging.DEBUG)
  unittest.main()
