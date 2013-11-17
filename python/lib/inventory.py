from couch import *

class Dictionary(Couch):
  def __init__(self, name='dictionary', server='http://localhost:5984'):
    Couch.__init__(self, name, server=server)

  def size(self):
    return 
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
