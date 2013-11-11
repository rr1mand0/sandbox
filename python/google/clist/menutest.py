import unittest
import logging
import sys

class MenuTest(unittest.TestCase):
  menu = {}
  def setUp(self):
    logging.basicConfig (stream = sys.stderr)
    log = logging.getLogger ("MenuTest").setLevel(logging.DEBUG)
    self.menu = {
        'schedule':  [
          {
            'date': 'Oct 14, 2013',
            'meal': 'Dinner',
            'menu': ['sausage', 'brocoli salad', 'corn']
          },
          {
            'date': 'Oct 15, 2013',
            'meal': 'Dinner',
            'menu': ['chicken cacciatore', 'rice']
          },
          {
            'date': 'Oct 16, 2013',
            'meal': 'Dinner',
            'menu': ['sausage', 'brocoli salad', 'corn']
          },
          {
            'date': 'Oct 17, 2013',
            'date': 'Thursday',
            'meal': 'Dinner',
            'menu': ['pasta with boconcini']
          },
          {
            'date': 'Oct 18, 2013',
            'meal': 'Dinner',
            'menu': ['basil salmon', 'rice', 'cucumber salad']
          },
          {
            'date': 'Oct 19, 2013',
            'meal': 'Dinner',
            'menu': ['out for dinner']
          },
          {
            'date': 'Oct 20, 2013',
            'meal': 'Dinner',
            'menu': ['chicken cacciatore', 'rice']
          },
        ]
    }

    def printmenu(self):
      log.debug ('Hello')
      menuCalendar = Menu(self.menu)
      log.debug (menu)

def main(argv):
  print 'hello'
  logging.basicConfig (stream = sys.stdout)
  log = logging.getLogger ("MenuTest").setLevel(logging.DEBUG)
  log.error("hello")
  suite = unittest.TestLoader().loadTestsFromTestCase(MenuTest)
  unittest.TextTestRunner(verbosity=2).run(suite)

  #unittest.main()

if __name__ == '__main__':
  main(sys.argv)
