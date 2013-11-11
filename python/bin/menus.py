#!/usr/bin/python

import re
import sys
import couch
import json

'''
{
  'items': [
    {
  ]
}
'''

def main(argv):
  print ('Menus')

  c = couch.Couch('menu')
  menus = c.get_docs()
  unique_menu = {}
  for menu in menus['items']:
    p = re.match (r'.*(Dinner|dinner|lunch|Lunch):(.*)', menu['name'])
    if p and p.groups(0)[1].strip() != '':
      item = p.groups(0)[1].strip()
      if item and not unique_menu.has_key(item):
        unique_menu[item] = {
          'dates':[menu['date']]
        }
      else:
        unique_menu[item]['dates'].append(menu['date'])

  meal = couch.Couch('meals')

  for k,v in unique_menu.items():
    meal.save({k:v})

if __name__ == "__main__":
   main(sys.argv[0:])
