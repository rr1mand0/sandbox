"""
https://developers.google.com/google-apps/tasks/v1/reference/tasklists#resource

{
  "kind": "tasks#taskList",
  "id": string,
  "etag": string,
  "title": string,
  "updated": datetime,
  "selfLink": string
}
"""

class TaskList:
  tasklist = {}

  def __init__ (self, tasklist, title):
    self.servicetasklist = tasklist
    self.title = title

  def get_id(self):
    result = self.servicetasklist.list().execute()
    i=0
    while True:
      try:
        mytitle = result['items'][i]['title']
        if mytitle == self.title:
          return result['items'][i]['id']
        pass
      except IndexError:
        return None
      i = i+1

  def exists(self):
    if self.get_id() == None:
      return False
    return True

  def insert(self):
    if not self.exists():
      #print "Inserting tasklist: %s"%self.title
      self.tasklist['title'] = self.title
      self.servicetasklist.insert(body=self.tasklist).execute()

  def delete(self):
    if self.exists():
      #print "Deleting tasklist %s"%self.title
      id = self.get_id()
      self.servicetasklist.delete(tasklist=id).execute()

  def dump(self):
    result = self.servicetasklist.list().execute()
    print json.dumps(result)

