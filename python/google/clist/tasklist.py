class TaskList:
  tasklist = {}

  def __init__ (self, tasklist, title):
    self.servicetasklist = tasklist
    self.title = title

  def GetId(self):
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

  def Exists(self):
    if self.GetId() == None:
      return False
    return True

  def Insert(self):
    if not self.Exists():
      print "Inserting tasklist: %s"%self.title
      self.tasklist['title'] = self.title
      self.servicetasklist.insert(body=self.tasklist).execute()

  def Delete(self):
    if self.Exists():
      print "Deleting tasklist %s"%self.title
      id = self.GetId()
      self.servicetasklist.delete(tasklist=id).execute()
