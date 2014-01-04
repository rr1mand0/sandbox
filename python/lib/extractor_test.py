import sys
import os
import logging
import unittest
from extractor import *

def read_html_file(filename):
  with open (filename, 'r') as f:
    data = f.read()
  return data

class ExtractorTest(unittest.TestCase):
  def test_domain(self):
    self.assertIsNotNone (Recipe('www.foodnetwork.com'))
    self.assertIsNotNone (Recipe('www.allrecipe.com'))

  @unittest.skip ('')
  def test_foodnetwork(self):
    fn_data = read_html_file('data/foodnetwork.html')
    fn = RecipeExtractor(fn_data)
   
    self.assertEqual(fn.title, 'Vegetable Tempura 3 Recipe')
    self.assertEqual(fn.domain, 'FoodNetwork')
    self.assertEqual(fn.ingredients.__len__, 10)


if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.DEBUG)
  sys.exit(unittest.main())
