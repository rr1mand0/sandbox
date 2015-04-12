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

  def scrape(self, url, keywords=None, save_to_es=False):
    parsed_uri = urlparse( url )
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    page = requests.get(url)
    recipe_tree = html.fromstring(page.text)

    if re.search('allrecipes.com', domain):
      recipe = AllrecipesScraper().extract(url, recipe_tree)
    elif re.search('about.com', domain):
      recipe = AboutScraper().extract(url, recipe_tree)
    elif re.search('foodnetwork.ca', domain):
      recipe = FoodnetworkCaScraper().extract(url, recipe_tree)
    elif re.search('chow.com', domain):
      recipe = ChowComScraper().extract(url, recipe_tree)

    if keywords:
      recipe['keywords'] = keywords

    if save_to_es:
      try:
        print json.dumps(recipe, indent=2)
        esfd = es.EsRecipe()
        esfd.save(recipe)
      except UnboundLocalError:
        print "Could not handle recipe from %s" % url
    return recipe

  def load(self, url):
    pass

  def list(self, **kwargs):
    esfd = es.EsRecipe()
    records = esfd.get_records()
    recipes = []
    for record in records:
      recipes.append(record['_source']['name'])
    print recipes
    return recipes

    

  def delete(self, url):
    esfd = es.EsRecipe()
    esfd.delete(url=url)

