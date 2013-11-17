import unittest
import re
import sys
from couch import *
import json

class TestThesaurus(unittest.TestCase):

  def setUp(self):
    self._thesaurus = {
      "cabage" : "cabbage",
      "cabagge" : "cabbage",
      "tom's": "tomatoes",
      "toms": "tomatoes",
      "tom": "tomatoes",
      "tomato": "tomatoes",
      "tomatoe": "tomatoes",
      "tomatos": "tomatoes",
      "veggie" : "veggies"
    }

    self.thes_dict = Thesaurus("test-thesaurus")

  def tearDown(self):
    pass
    #self.thes_dict.destroy()


  def test_add_definition(self):
    self.thes_dict.set_thesaurus(self._thesaurus)
    self.thes_dict.save()

    synonyms = self.thes_dict.get_synonyms('tomatoes')

    self.assertNotEqual(synonyms, None) 
    self.assertTrue(synonyms.__len__(), 6)
    self.thes_dict.add_synonym("vegetables", "veggies")



if __name__ == '__main__':
  unittest.main()
