from googleservice import GoogleService
import sys
import json


def main(argv):
  def get_ingredients(recipe):
    result = tasklists.list().execute()
    i = 0
    while True:
      try:
        mytitle = result['items'][i]['title']
        print ("     %s == %s"%(mytitle.strip(), recipe.strip()))
        if mytitle.strip() == recipe.strip():
          id = result['items'][i]['id'],
          print ("    ingredient: %s %s" % (result['items'][i]['id'], recipe))
          id = result['items'][i]['id']
          break
      except IndexError:
        #print ("%s: not found" % (recipe))
        return None
      i = i+1

    #shoppingListId = taskService.tasklists().get(tasklist="shoppingList").execute()


    item = {
      'title': 'Cuccumber',
      'notes' : 'x3'
    }

    id = tasks.insert(tasklist=id, body=item).execute()

  title = 'shoppingList'
  calendarName = 'Menu'
  service = GoogleService()

  calendar_service = GoogleService().get_calendar_service()
  calendarlist     = calendar_service.calendarList()

  task_service     = GoogleService().get_task_service()
  tasklists        = task_service.tasklists()
  tasks            = task_service.tasks()

  page_token = None
  while True:
    calendar_list = calendarlist.list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      if calendar_list_entry['summary'] == calendarName:
        calendar_id = calendar_list_entry
        print calendar_list_entry['summary']
        break
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break

  print ("calendarId = %s"%calendar_id['id'])
  page_token = None

  from datetime import tzinfo, timedelta, datetime
  d = "%sZ"%datetime.now().isoformat('T')
  #d = '2013-01-01T00:00:00Z'
  while True:
    events = calendar_service.events().list(
        orderBy = 'updated', 
        showDeleted = False, 
        calendarId=calendar_id['id'], 
        pageToken=page_token,
        timeMin = d , 
        q = 'Dinner').execute()
    for event in events['items']:
      #if event.get('start'):
      recipes = event['summary'].split(":")[1]
      print ("meal: %s" % recipes)
      for recipe in recipes.split(","):
        print ("  recipe: %s"%(recipe))
        get_ingredients(recipe)
    page_token = events.get('nextPageToken')
    if not page_token:
      break



if __name__ == '__main__':
  main(sys.argv)
