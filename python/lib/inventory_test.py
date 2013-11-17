import unittest
from couch import *
from inventory import *

class TestThesaurus(unittest.TestCase):
  def test_one(self):
    self.assertEqual(1,1)

  def test_create_keyword(self):
    dictionary = Dictionary(name='test-dictionary')
    dictionary.addTerm({'carrots': ['carots', 'carrot']})
    dictionary.addTerm({'tomatoes': ['tomato', 'tomatos']})

    self.assertEqual(dictionary.size(), 2)

if __name__ == '__main__':
    unittest.main()

