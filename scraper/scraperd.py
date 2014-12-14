import web
import json
from elasticsearch import Elasticsearch

# /products/diaper {}
_URLS = (
    "/products", "ProductsHandler",
    "/products/([^/]+)", "ProductsHandler",
    "/scraper/scrape/(.+)", "Scraper",
    "/", "RootHandler"
    )


class Products(object):
  def __init__(self):
    self._es = Elasticsearch()

  def publish(self, body):
    self._es.index(index='products', doc_type='product', body = body)

class ProductsHandler(object):
  def GET(self, _=None):
    hits = Elasticsearch().search(index='products')['hits']['hits']
    values = []
    for v in hits:
      values.append(v['_source']['world'])
    return json.dumps(values, indent=2)

  def POST(self):
    args = web.data()
    jstring = json.loads(args)
    Products().publish(jstring)

class Scraper(object):
  def GET(self, name):
    return name

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__ == "__main__":
    app = MyApplication(_URLS, globals(), autoreload=True)
    app.run(port=8888)

