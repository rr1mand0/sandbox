import os
import argparse
import json
import sys
import logging
#from recipe import Recipe
import couch

SERVER = 'http://localhost:5984'
DBNAME = 'recipes'

def listfn(args):
  _recipe = couch.Recipes(server = SERVER, dbname = DBNAME)
  print ("%s" % json.dumps( _recipe.get_docs(), indent=2))

def addfn(args):
  _recipe = couch.Recipes(server = SERVER, dbname = DBNAME)
  _recipe.add_with_ingredients(args.add_recipe, ingredients = args.ingredients)

def deletefn(args):
  _recipe = couch.Recipes(server = SERVER, dbname = DBNAME)
  _recipe.delete(args.delete_recipe)

def showfn(args):
  _recipe = couch.Recipes(server = SERVER, dbname = DBNAME)
  _recipe.show(args.show_recipe)
# Main
if __name__ == '__main__':

  def run():
    _recipe = couch.Recipes(server = SERVER, dbname = DBNAME)
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_add = subparsers.add_parser('add',
      help='add a recipe')
    parser_add.add_argument("add_recipe", help="recipe to add",
      type=str)
    parser_add.add_argument('-i', '--ingredients',
      help='ingredients for recipe')
    parser_add.set_defaults(func=addfn)

    parser_delete = subparsers.add_parser('delete',
      help='delete recipes')
    parser_delete.add_argument("delete_recipe", help="recipe to delete",
      type=str)
    parser_delete.set_defaults(func=deletefn)

    parser_show = subparsers.add_parser('show',
          help='delete recipes')
    parser_show.add_argument("show_recipe", help="recipe to show",
                        type=str)
    parser_show.set_defaults(func=showfn)

    parser_list = subparsers.add_parser('list',
          help='list recipes')
    parser_list.set_defaults(func=listfn)

    args = parser.parse_args()

    return args.func(args)

  logging.basicConfig(filename='%s/recipe.log' % os.environ['LOG_DIR'], level=logging.INFO)
  sys.exit(run())

