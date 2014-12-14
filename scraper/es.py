from elasticsearch import Elasticsearch

class EsRecipe(object):
  def __init__(self, 
      server = "localhost", 
      port = 9200,
      index = "recipes",
      doc_type = "recipe-type"):
    self._port = port
    self._server = server
    self._es = Elasticsearch()
    self._index = index
    self._doc_type = doc_type

  def _search(self, **kwargs):
    if 'url' in kwargs:
      body = {'query':{'match':{'url':kwargs['url']}}}

    if body is not None:
      try:
        resp = self._es.search(index=self._index, doc_type=self._doc_type, body=body)
        return resp['hits']['hits'][0]['_id']
      except IndexError:
        return None
    return None

  def delete(self, **kwargs):
    if 'id' in kwargs:
      id = kwargs['id']
    elif 'url' in kwargs:
      id = self._search(url=kwargs['url'])

    resp = self._es.delete(index=self._index, doc_type=self._doc_type, id=id)

  def save(self, recipe):
    id=self._search(url=recipe['url'])
    if id:
      rc = self._es.update(index=self._index, 
                           doc_type=self._doc_type, 
                           id=id, 
                           body={'doc':recipe})
    else:
      rc = self._es.index(
          index = self._index,
          doc_type = self._doc_type,
          body = recipe)

