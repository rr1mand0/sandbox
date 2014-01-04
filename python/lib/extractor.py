from bs4 import BeautifulSoup

class RecipeExtractor(object):
  @classmethod
  def is_registrar_for(cls, domain):
    return domain == cls.name

  title = None
  ingredients = []
  def __init__(self, domain):
    self.domain = domain

  def identify(self):
    pass

  def parse(self):
    pass

  def get_recipe_name(self):
    pass

  def get_ingredients(self):
    pass

class FoodNetworkExtractor(RecipeExtractor):
  name = 'www.foodnetwork.com'

class AllRecipeExtractor(RecipeExtractor):
  name = 'www.allrecipe.com'

def Recipe(domain):
  for cls in RecipeExtractor.__subclasses__():
    if cls.is_registrar_for(domain):
      return cls(domain)
  raise ValueError


print Recipe('www.foodnetwork.com')
print Recipe('www.allrecipe.com')
