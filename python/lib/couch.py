import couchdb

class Couch(object):
  def __init__(self, dbname, server='http://192.168.1.104:8081'):
    couch = couchdb.Server(server)

    # try and create a database
    try:
      self.db = couch.create(dbname.lower()) 
    except couchdb.http.PreconditionFailed:
      pass
    self.db = couch[dbname.lower()]



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

  def save(self, item):
    self.db.save(item)
