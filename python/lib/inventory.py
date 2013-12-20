from couch import *

class Dictionary(Couch):
  #def __init__(self, 'http://localhost:5984', 'dictionary'):
  def __init__(self, server, dbname):
    Couch.__init__(self, server, dbname)

  def __len__(self):
    return self.db.__len__()

  def addTerm(self, term):
    if term:
      self.db.save (
          {
            'name': term.keys(),
            'values': term.values()
          }
        )




class Inventory(Couch):
  def __init__(self):
    print "hello"
