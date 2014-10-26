from lxml import html
import json
import sys
import argparse
import requests
from urlparse import urlparse



class RecipeScraper(object):
  def __init__(self):
      pass

class AboutScraper(RecipeScraper):
  @staticmethod
  def extract(url, recipe_tree):
    title = recipe_tree.xpath('//h1/text()')
    ingredients = recipe_tree.xpath('//*[@itemprop="ingredients"]/text()')
    return {
            'name': title,
            'ingredients': ingredients,
            'url': url
            }

class AllrecipesScraper(RecipeScraper):
  @staticmethod
  def extract(url, recipe_tree):
    title = recipe_tree.xpath('//h1/text()')
    quantity = recipe_tree.xpath('//span[@class="ingredient-amount"]/text()')
    ingredients = recipe_tree.xpath('//span[@class="ingredient-name"]/text()')

    return {
            'name': title,
            'ingredients': map ( 
                lambda pair: "%s %s" % (pair), 
                zip(quantity, ingredients)),
            'url': url
            }

class FoodnetworkCaScraper(RecipeScraper):
  @staticmethod
  def extract(url, recipe_tree):
    title = recipe_tree.xpath('//h1/text()')
    ingredients = recipe_tree.xpath('.//p[@itemprop="ingredients"]/text()')

    return {
            'name': title,
            'ingredients': map (
                lambda string: ' '.join(string.split()), 
                    ingredients),
            'url': url
            }

class ChowComScraper(RecipeScraper):
  @staticmethod
  def extract(url, recipe_tree):
    title = recipe_tree.xpath('//h1/text()')
    ingredients = recipe_tree.xpath('.//span[@itemprop="name"]/text()')
    quantity = recipe_tree.xpath('.//span[@itemprop="amount"]/text()')

    return  {
            'name': title,
            'ingredients': map ( 
                lambda pair: "%s %s" % (pair), 
                zip(quantity, ingredients)),
            'url': url
            }


def scrape(args):
  parsed_uri = urlparse( args.url )
  domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

  page = requests.get(args.url)
  recipe_tree = html.fromstring(page.text)

  if domain == 'http://allrecipes.com/':
    recipe = AllrecipesScraper().extract(args.url, recipe_tree)
  elif domain == 'http://bbq.about.com/':
    recipe = AboutScraper().extract(args.url, recipe_tree)
  elif domain == 'http://www.foodnetwork.ca/':
    recipe = FoodnetworkCaScraper().extract(args.url, recipe_tree)
  elif domain == 'http://www.chow.com/':
    recipe = ChowComScraper().extract(args.url, recipe_tree)

  try:
    print json.dumps(recipe, indent=2)
  except UnboundLocalError:
    print "Could not handle recipe from %s" % args.url



def main():
  parser = argparse.ArgumentParser(description="recipe scraper toolset")

  parser.add_argument('-v', '--verbose', action='store_true', default=False,
      help='verbose output' )
  subparsers = parser.add_subparsers(help='sub-command help')

  parser_scrape = subparsers.add_parser('scrape', 
      help='search for accounts matching string.  To print all accounts you can use "all"')
  parser_scrape.add_argument ('url', help='url to scrape')
  parser_scrape.set_defaults(func=scrape)
  
  args = parser.parse_args()
  args.func(args)

if __name__ == '__main__':
  sys.exit(main())
