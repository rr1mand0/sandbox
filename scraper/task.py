import googleservice as gs
import sys
import argparse
import json

def tl_list(args):
  tasklist = gs.TaskService().get_tasklist()
  for n in tasklist['items']:
    print n['title']

def tl_create(args):
  gs.TaskService().create(args.listname)

def tl_delete(args):
  gs.TaskService().delete(args.listname)

def main():
  parser = argparse.ArgumentParser(description='Task list manager')

  tasklist_subparser = parser.add_subparsers(help='sub-command help')

  tl_parser_list = tasklist_subparser.add_parser('list',
      help='list taskslists')
  tl_parser_list.set_defaults(func=tl_list)

  tl_parser_create = tasklist_subparser.add_parser('create',
      help='adds a taskslist')
  tl_parser_create.add_argument('listname')
  tl_parser_create.set_defaults(func=tl_create)

  tl_parser_delete = tasklist_subparser.add_parser('delete',
      help='delete a taskslist')
  tl_parser_delete.add_argument('listname')
  tl_parser_delete.set_defaults(func=tl_delete)

  args = parser.parse_args()
  args.func(args)
  


if __name__ == '__main__':
  sys.exit(main())
