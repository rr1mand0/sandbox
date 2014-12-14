from lxml import html
import re
import json
import requests
from urlparse import urlparse
import es


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



class Scraper(object):
  def __init__(self):
    esfd = es.EsRecipe()

  def scrape(self, url):
    parsed_uri = urlparse( args.url )
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    page = requests.get(args.url)
    recipe_tree = html.fromstring(page.text)

    if re.search('allrecipes.com', domain):
      recipe = AllrecipesScraper().extract(args.url, recipe_tree)
    elif re.search('about.com', domain):
      recipe = AboutScraper().extract(args.url, recipe_tree)
    elif re.search('foodnetwork.ca', domain):
      recipe = FoodnetworkCaScraper().extract(args.url, recipe_tree)
    elif re.search('chow.com', domain):
      recipe = ChowComScraper().extract(args.url, recipe_tree)

    try:
      print json.dumps(recipe, indent=2)
      esfd = es.EsRecipe()
      esfd.save(recipe)
    except UnboundLocalError:
      print "Could not handle recipe from %s" % args.url

  def load(self, url):
    pass

  def delete(self, url):
    esfd = es.EsRecipe()
    esfd.delete(url=url)

