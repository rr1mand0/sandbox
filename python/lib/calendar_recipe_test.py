import unittest
import logging
import os

class ShoppingListCreator(unittest.TestCase):
  def test_create_shopping_list_from_calendar(self):
    self.assertIsNotNone({})

if __name__ == '__main__':
  logging.basicConfig(filename='%s/test.log' % os.environ['LOG_DIR'], level=logging.INFO)
  unittest.main()

