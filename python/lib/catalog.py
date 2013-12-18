# catalog = {
#  'food basics_eramosa' : {
#    'inventory': [
#      '0123456789': {
#        'price': 1.69
#      }
#    ] 
#  },
#  'zehrs_eramosa': {
#    'inventory': {
#      '0123456789': {
#        'price': 1.99
#      }
#    }
#  }
# }
#
# product = {
#   'sku': 0123456789,
#   'norm_name: 'gala apples'
# }
#
# dictionary = {
#   'apple': ['apples', 'aples']
# }
class Catalog(object):
  catalog = {}
  def __init__(self, name):
    print ("Creating catalog: %s", name)

  def getlocation(self, store):
    return '%s-%s' % (store['name'], store['location'])

  def add(self, item, store, price, sku=None, unit=None):
    print ("adding %s" % ( item ))
    self.catalog[self.getlocation(store)] = {'hello'}


  def price_by_name(self, name, store):
    return self.catalog[self.getlocation(store)]['inventory'][name]
