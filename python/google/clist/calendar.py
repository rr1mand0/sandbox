import json

class Calendar:
  def __init__(self, service, calendar_name):
    self.service = service
    self.calendar_name = calendar_name
    pass

  def get_id(self):
    page_token = None
    try:
      calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
      #print json.dumps(calendar_list, indent=2)
    except:
      pass
    i=0
    while True:
      try:
        mytitle = calendar_list['items'][i]['summary']
        if mytitle == self.calendar_name:
          return calendar_list['items'][i]['id']
        pass
      except IndexError:
        return None
      i = i+1

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
