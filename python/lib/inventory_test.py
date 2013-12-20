import unittest
from couch import *
from inventory import *

class TestThesaurus(unittest.TestCase):
  def setUp(self):
    self.dictionary = Dictionary('http://localhost:5984', 'test-dictionary')

  def tearDown(self):
    self.dictionary.destroy()

  def test_one(self):
    self.assertEqual(1,1)

  def test_create_keyword(self):
    self.dictionary.addTerm({'carrots': ['carots', 'carrot']})
    self.dictionary.addTerm({'tomatoes': ['tomato', 'tomatos']})

    self.assertEqual(self.dictionary.__len__(), 2)

if __name__ == '__main__':
    unittest.main()

