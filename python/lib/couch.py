import re
import sys
import couchdb
import json

class Couch(object):
  def __init__(self, dbname, server='http://192.168.1.104:8081', create=False):
    couch = couchdb.Server(server)

    # try and create a database
    try:
      self.db = couch.create(dbname.lower()) 
      print ("Creating database %s" % dbname)
    except couchdb.http.PreconditionFailed:
      print ("Exists database %s" % dbname)
      pass
    self.db = couch[dbname.lower()]
    print self.db

  def create(self):
    try:
      self.db = couch.create(dbname.lower()) 
    except couchdb.http.PreconditionFailed:
      pass

  def destroy(self):
    pass

  def get_docs(self):
    map_fun = '''function(doc) {
      if (doc.summary) {
        emit(doc.summary, doc.start.date);
      }
    }'''
    
    docs = []
    for row in self.db.query(map_fun):
      doc = {
          'name': row.key,
          'date': row.value
          }
      docs.append(doc)
    return {'items':docs}

  def load(self):
    pass

  def save(self, item):
    
    self.db.save(item)

  def pprint(self, json_in):
    print json.dumps(json_in, indent=2, sort_keys=True)

class Thesaurus(Couch):
  normalized = {
    "cabbage" : ['cabage'],
    "tomatoes": ['tom\'s', 'tomatos', 'tomato', 'tomatoe'],
    "veggies" : ['veggie']
  }

  def __init__(self, name='thesaurus'):
    Couch.__init__(self, name)

  def set_thesaurus(self, _thesaurus):
    self.thesaurus = _thesaurus

  def get_normalized(self, word):
    return self.thesaurus.get(word, None)

  def add_synonym(self, word, syn):
    if not self.thesaurus.has_key(word):
      self.thesaurus[word] = syn

  def normalized_to_thesaurus(self, normalized):
    _the = {}
    for k,v in normalized.items():
      for word in v:
        _the[word] = k
    return _the

  def thesaurus_to_normalized(self):
    _norm = {}
    for k,v in self.thesaurus.items():
      if not _norm.has_key(v):
        _norm[v] = [k]
      else:
        _norm[v].append(k)
    return _norm


  ''' 
  returns a hash of: acroynm : keyword
  thesaurus = {
    'gr beans' : "green beans"
  }'''
  def load(self):
    pass

  def get_normalized(self, word):
    return self.thesaurus.get(word, None)

  ''' 
    saves as
    keyword: [array of acronyms]
  thesaurus = {
    'cabbage' : [ 'cabage', 'cabagge' ]
  }'''
  def save(self):
    # transform into keyword: [acryonmns]
    print self.db
    normalized = self.thesaurus_to_normalized()
    for k,v in normalized.items():
      i = {
        'name': k,
        'values': v
      }
      self.pprint(i)


class Recipes(Couch):
  def __init__(self):
    Couch.__init__(self, 'recipes')
    self.recipes = {}

  def add(self, recipe):
    self.recipes[recipe] = {
      'name': recipe,
      'ingredients': []
    }

  def parse(self, str):
    for recipe in str.split(','):
      self.add(recipe.strip())


class Menu(Couch):
  def __init__(self):
    Couch.__init__(self, 'menu')

  def process(self):
    menus = self.get_docs()
    self.unique_menu = {}
    for menu in menus['items']:
      p = re.match (r'.*(Dinner|dinner|lunch|Lunch):(.*)', menu['name'])
      if p and p.groups(0)[1].strip() != '':
        item = p.groups(0)[1].strip()
        if item and not self.unique_menu.has_key(item):
          self.unique_menu[item] = {
            'name': item,
            'dates':[menu['date']]
          }
        else:
          self.unique_menu[item]['dates'].append(menu['date'])

  def get_unique_menu(self):
    return self.unique_menu

  def save(self, db):
    meal = Couch(db)

    for k,v in self.unique_menu.items():
      meal.save({
        'name':k,
        'dates': v['dates']
        })
