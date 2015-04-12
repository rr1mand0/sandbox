import googleservice as gs
import sys
import argparse
import json
from datetime import datetime, timedelta
from tabulate import tabulate
import pytz
from datetime import datetime
import scrape


def cal_list(args):
  callist = gs.CalendarService().get_calendarlist()
  table = []
  for n in callist['items']:
    table.append([n['id'], n['summary']])
  print tabulate(table)

def cal_create(args):
  gs.CalendarService().create(args.calendar)

def cal_delete(args):
  gs.CalendarService().delete(args.calendar)

def cal_show(args):

  table = []
  start_time = datetime.utcnow().replace(tzinfo = pytz.utc)
  end_time = start_time + timedelta(days=args.duration)
  
  events = gs.CalendarService().get_calendar_events(args.calendar, start_time.isoformat(), end_time.isoformat())

  for event in events:
    if event.has_key('description'):
      table.append([event['start']['date'], event['summary'], event['description']])
    else:
      table.append([event['start']['date'], event['summary'], ""])

  print tabulate(table)

def cal_export(args):

  start_time = datetime.utcnow().replace(tzinfo = pytz.utc)
  end_time = start_time + timedelta(days=args.duration)
  
  events = gs.CalendarService().get_calendar_events(args.calendar, start_time.isoformat(), end_time.isoformat())
  recipes = []

  for event in events:
    if event.has_key('description'):
      recipe = scrape.Scraper().scrape(event['description'])
    else:
      recipe = {
        "name": event['summary']
      }
    recipes.append(recipe)

  tl = gs.TaskService().create(args.tasklist)
  for recipe in recipes:
    body = {
      'title': recipe['name'],
      'notes': None
    }

    task_recipe = gs.TaskService().service.tasks().insert(tasklist=tl['id'], body=body).execute()

    if recipe.has_key('ingredients'):
      for ingredient in recipe['ingredients']:
        body = {
          'title': ingredient
        }
        task = gs.TaskService().service.tasks().insert(tasklist=tl['id'], body=body, parent=task_recipe['id']).execute()


  print json.dumps(recipes, indent=2)


def main():
  parser = argparse.ArgumentParser(description='Task list manager')
  parser.add_argument('--json', action='store_false')

  calendar_subparser = parser.add_subparsers(help='sub-command help')

  cal_parser_list = calendar_subparser.add_parser('list',
      help='list taskslists')
  cal_parser_list.set_defaults(func=cal_list)

  cal_parser_create = calendar_subparser.add_parser('create',
      help='adds a taskslist')
  cal_parser_create.add_argument('calendar')
  cal_parser_create.set_defaults(func=cal_create)

  cal_parser_delete = calendar_subparser.add_parser('delete',
      help='delete a taskslist')
  cal_parser_delete.add_argument('calendar')
  cal_parser_delete.set_defaults(func=cal_delete)

  cal_parser_show = calendar_subparser.add_parser('show',
      help='show calendar')
  cal_parser_show.add_argument('calendar')
  cal_parser_show.add_argument('--start-time', default=0, help='Starting date to show')
  cal_parser_show.add_argument('--duration', default=7, help='Days to show from start-time')
  cal_parser_show.add_argument('--to-tasks', default=None, help='Save the recipes to tasks')
  cal_parser_show.set_defaults(func=cal_show)

  cal_parser_export = calendar_subparser.add_parser('export',
      help='export calendar to tasks')
  cal_parser_export.add_argument('calendar')
  cal_parser_export.add_argument('tasklist')
  cal_parser_export.add_argument('--start-time', default=0, help='Starting date to show')
  cal_parser_export.add_argument('--duration', default=7, help='Days to show from start-time')
  cal_parser_export.set_defaults(func=cal_export)

  args = parser.parse_args()
  args.func(args)
  


if __name__ == '__main__':
  sys.exit(main())
