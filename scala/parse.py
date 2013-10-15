import json
import re

def write_hash_as_file(data, outfile):
  print ("Writing %s" % outfile)
  f = open ("tmp/%s"%outfile, 'w')
  f.write (data)
  f.close()

def get_array_from_file(file, title):
  raw = open(file, 'r')
  catalog = {title: []}
  for line in raw:
    catalog[title].append(json.loads(line.rstrip('\n')))
  return catalog

products = get_array_from_file('products.txt', 'products')
#print products

listings = get_array_from_file('listings.txt', 'listings')

manufacturers = set([])

for m_product in products['products']:
  if m_product.has_key('manufacturer') and not m_product['manufacturer'] in manufacturers:
    manufacturers.add(m_product['manufacturer'])

  m_product['listing'] = []
  for m_listing in listings['listings']:
    if m_listing.has_key('manufacturer') and not m_listing['manufacturer'] in manufacturers:
      manufacturers.add(m_listing['manufacturer'])
    if m_product['manufacturer'] == m_listing['manufacturer']:
      pattern = re.compile(r"\b%s\b" % m_product['model'])

      if pattern.search(m_listing['title']):
        m_product['listing'].append(m_listing)
        listings['listings'].remove(m_listing)

  
write_hash_as_file(json.dumps(products, indent=2), "merged.txt")
write_hash_as_file(repr(sorted(manufacturers)), "manufacturers.txt")

#print '%s'%(json.dumps(products, indent=2))


