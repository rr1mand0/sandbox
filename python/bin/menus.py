#!/usr/bin/python

import re
import sys
from couch import *
import json

'''
{
  'items': [
    {}
  ]
}
'''

thesaurus = {
  "cabage" : "cabbage",
  "cabagge" : "cabbage",
  "stirfry" : "stir fry",
  "tom's": "tomatoes",
  "toms": "tomatoes",
  "tom": "tomatoes",
  "tomato": "tomatoes",
  "tomatoe": "tomatoes",
  "tomatos": "tomatoes",
  "veggie" : "veggies",
  "vietnames": "vietnamese"
}

def main(argv):
  _old_menu = Menu()
  _old_menu.process()
  menu = _old_menu.get_unique_menu()

  recipes = {}

  thes_dict = Thesaurus()
  thes_dict.set_thesaurus(thesaurus)

  thes_dict.add_synonym("vegetables", "veggies")

  for meal in menu:
    for recipe in meal.split(','):
      recipe_name = recipe.strip().lower()
      recipes[recipe_name] = {}
      for word in re.split(';|,| |\+|w/|/|\(|\)|<|>|\[|\]|-', recipe_name):
        thes_dict.add_synonym(word, word)

  for word in ["vietnames", "tomatoe", "vegetables"]:
    print ("lookup: %s %s" % (word, thes_dict.get_normalized(word)))

  normalized = thes_dict.thesaurus_to_normalized()
  thes_dict.normalized_to_thesaurus(normalized)

  thes_dict.save()

if __name__ == "__main__":
   main(sys.argv[0:])
