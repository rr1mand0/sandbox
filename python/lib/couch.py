import logging
import re
import sys
import couchdb
import json

class Couch(object):
  def __init__(self, server, dbname, create=False):
    self.couch = couchdb.Server(server)
    self.dbname = dbname.lower()

    # try and create a database
    try:
      self.db = self.couch.create(self.dbname) 
      logging.debug ("Created database %s" % self.dbname)
    except couchdb.http.PreconditionFailed:
      pass
    self.db = self.couch[self.dbname]
    #logging.debug (self.db)

  def create(self):
    try:
      self.db = self.couch.create(self.dbname) 
    except couchdb.http.PreconditionFailed:
      pass

  def destroy(self):
    self.db = self.couch.delete(self.dbname) 
    logging.debug ("Deleting database %s" % self.dbname)

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
    logging.debug ("%s" % json.dumps(json_in, indent=2, sort_keys=True))

class Thesaurus(Couch):
  normalized = {
    "cabbage" : ['cabage'],
    "tomatoes": ['tom\'s', 'tomatos', 'tomato', 'tomatoe'],
    "veggies" : ['veggie']
  }

  def __init__(self, server, name='thesaurus'):
    Couch.__init__(self, server, name)

  def set_thesaurus(self, _thesaurus):
    self.thesaurus = _thesaurus
    self._normalized = self.thesaurus_to_normalized()
    self.pprint(self._normalized)

  def get_synonyms(self, word):
    return self._normalized.get(word, None)

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
    logging.debug ("%s" % self.db)
    normalized = self.thesaurus_to_normalized()
    for k,v in normalized.items():
      i = {
        'name': k,
        'values': v
      }
      logging.debug ('%s' % self.db.save(i))


def mangled_id(string):
  return string.replace(" ", "_").lower()

class Recipes(Couch):
  def __init__(self, server='http://localhost:5984', dbname='recipes'):
    Couch.__init__(self, server, dbname)
    self.recipes = {}

  def add_with_ingredients (self, name, ingredients = []):
    self.add({
      'name': name,
      'ingredients': [ing.strip() for ing in ingredients.split(',')]
    })
    
  def add(self, recipe):
    if recipe:
      doc = self.get_doc(recipe['name'])
      if doc:
        recipe['_rev'] = doc['_rev']
        recipe['_id'] = doc['_id']

      rev_id, rev_ver = self.db.save(recipe)
      logging.info("Adding recipe: %s (%s -- %s)" % (recipe['name'], rev_id, rev_ver))
      logging.debug("recipe: %s:\n%s" % (recipe['name'], json.dumps(recipe, indent=2)))

  def update(self, recipe):
    return self.add(recipe)

  def exists(self, name):
    if self.get_doc(name):
      return True
    return False

  def get_id(self, name):
    for id in self.db:
      if name == self.db[id]['name']:
        return id
    return None

  def get_doc(self, name):
    for id in self.db:
      if name == self.db[id]['name']:
        logging.debug("get_doc: %s" % (json.dumps(self.db[id],indent=2)))
        return self.db[id]
    return {}

  def delete(self, name):
    for id in self.db:
      if self.db[id]['name'] == name:
        logging.info("Deleting recipe: %s" % json.dumps(self.db[id], indent=2))
        self.db.delete(self.db[id])

  def __len__(self):
    return self.db.__len__()

  def show(self, name):
    doc = self.get_doc(name)
    print("Recipe: %s"% json.dumps(doc, indent=2))

  def list(self, name):
    logging.info("List recipes")


  def get_docs(self):
    map_fun = '''function(doc) {
      if (doc._id) {
        emit(doc.name, doc._id);
      }
    }'''
    
    docs = []
    for row in self.db.query(map_fun):
      docs.append({ 'name': row.key, 'id': row.value })
    return {'items':docs}

  def parse(self, string):
    for recipe in string.split(','):
      self.add(recipe.strip())


class Menu(Couch):
  def __init__(self, server, name):
    Couch.__init__(self, server, name)

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
