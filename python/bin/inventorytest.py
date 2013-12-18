import unittest
from catalog import Catalog

class ServiceTest(unittest.TestCase):
  def test_AddInventory(self):
    price = 2.52
    item = {
      "name": "carrots",
      "unit": "kg",
      "price": price
    }
    store = {
      "name": "Zehrs",
      "location": "guelph"
    }

    c = Catalog("zehrs")
    c.add(item, store)
    self.assertEqual (c.price_by_store("carrots", store), price)

if __name__ == '__main__':
  unittest.main()

