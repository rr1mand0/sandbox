import json

class CalendarList:
  calendarList = {}
  def __init__(self, service, calendar_name):
    self.service = service
    self.calendar_name = calendar_name

  def get_id(self):
    page_token = None
    try:
      calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
      print json.dumps(calendar_list, indent=2)
    except:
      pass

    i=0
    while True:
      try:
        mytitle = calendar_list['items'][i]['summary']
        print "%s == %s"%(mytitle, self.calendar_name)
        if mytitle == self.calendar_name:
          return calendar_list['items'][i]['id']
        pass
      except IndexError:
        print "%s not found"%mytitle
        return None
      i = i+1

  def delete(self):
    id = self.get_id()
    if id != None:
      print "deleting %s:%s"%(self.calendar_name,id)
      self.service.calendarList().delete(id).execute()

  def insert(self):
    if not self.exists():
      print "inserting %s"%self.calendar_name
      #self.calendarList['summary'] = self.calendar_name
      calendar_list_entry = {
        'id' : 'calendarId'
      }
      created_calendar_list_entry = self.service.calendarList().insert(body=calendar_list_entry).execute()
      print created_calendar_list_entry['summary']
      
  def exists(self):
    if self.get_id() == None:
      return False
    return True

  def list(self):
    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      if calendar_list[self.calendar_name]:
        for calendar_list_entry in calendar_list[self.calendar_name]:
          print calendar_list_entry['summary']
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

  def get_calendar_items(self):
    pass


  def list_items(self):
    pass

