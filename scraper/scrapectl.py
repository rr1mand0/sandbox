import sys
import scrape
import argparse

def main():
  parser = argparse.ArgumentParser(description="recipe scraper toolset")

  parser.add_argument('-v', '--verbose', action='store_true', default=False,
      help='verbose output' )
  subparsers = parser.add_subparsers(help='sub-command help')

  parser_scrape = subparsers.add_parser('scrape', 
      help='search for accounts matching string.  To print all accounts you can use "all"')
  parser_scrape.add_argument ('url', help='url to scrape')
  parser_scrape.add_argument ('--keywords', nargs="+", help='url to scrape', default=[])
  parser_scrape.set_defaults(func=scrape.Scraper().scrape)

  parser_delete = subparsers.add_parser('delete', 
      help='search for accounts matching string.  To print all accounts you can use "all"')
  parser_delete.add_argument ('url', help='url to delete')
  parser_delete.set_defaults(func=scrape.Scraper().delete)
  
  args = parser.parse_args()
  args.func(url=args.url, keywords=args.keywords)

if __name__ == '__main__':
  sys.exit(main())
