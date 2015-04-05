import googleservice as gs
from tasks import Task
from oauth2client.client import AccessTokenRefreshError
import sys
import gflags
import unittest
import json
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

  def __init__ (self):
    self.task_service = gs.TaskService().service
    self.servicetasklist = self.task_service.tasklists()

  def get_id(self, title):
    result = self.servicetasklist.list().execute()
    i=0
    while True:
      try:
        mytitle = result['items'][i]['title']
        if mytitle == title:
          return result['items'][i]['id']
        pass
      except IndexError:
        return None
      i = i+1

  def exists(self, title):
    if self.get_id(title) == None:
      return False
    return True

  def create(self, title):
    import ipdb; ipdb.set_trace() # BREAKPOINT
    if not self.exists(title):
      #print "Inserting tasklist: %s"%self.title
      self.tasklist['title'] = title
      self.servicetasklist.insert(body=self.tasklist).execute()

  def delete(self, title):
    if self.exists(title):
      #print "Deleting tasklist %s"%self.title
      id = self.get_id(title)
      self.servicetasklist.delete(tasklist=id).execute()

  def dump(self):
    result = self.servicetasklist.list().execute()
    print json.dumps(result)

