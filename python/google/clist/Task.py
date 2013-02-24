# -*- coding: utf-8 -*-

import datetime
import gflags
import httplib2
import logging
import os
import pprint
import sys
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


FLAGS = gflags.FLAGS
CLIENT_SECRETS = 'client_secrets.json'

# Helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to download the client_secrets.json file
and save it at:

%s

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope=[
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/tasks.readonly',
    ],
    message=MISSING_CLIENT_SECRETS_MESSAGE)


# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')



class GoogleAuth(object):
  def __init__(self):
    storage = Storage('sample.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
      credentials = run(FLOW, storage)

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    self.service = build('tasks', 'v1', http=http)

#   try:
#     result = self.service.tasklists().list().execute()
#     #pprint.pprint (result)
#     for item in result["items"]:
#       print ("List found: " + item["title"] + " >> " + item["id"])

#     result = self.service.tasks().list(tasklist='MTAyNTg4OTUzODQ0MzM5NDgxOTQ6MjAxMjI4NzM1NDow').execute()
#     for item in result["items"]:
#       print (">> List found: " + item["title"] + " >> " + item["id"])
#   except:
#     pass

  def getService(self):
    return self.service

class Task(object):
  _title = None
  def __init__(self, title):
    self._title = title
    pass

  def getBody(self):
    return { 'title' : self._title }

class TaskList(GoogleAuth):
  _tasklist = None
  _kind = "tasks#taskList"
  _updated = None
  _etag = None
  _id = None
  _selfLink = None
  

  def __init__(self, title):
    self._title = title

    # authenticate 
    GoogleAuth.__init__(self)
    #self.FindTaskList()
    self.CreateIfNotExists(title)
    pass

  def FindTaskList(self):
    self._tasklist = GoogleAuth.getService(self).tasks().list(tasklist='@default')
    pprint.pprint (self._tasklist)
    if self._tasklist:
      print "Found tasklist: " + self._title
      #result = GoogleAuth.getService(self).tasks().list(tasklist=self._tasklist['id']).execute()
      #pprint.pprint (result)
    else:
      print ("Creating: " + self._title)
      _body = { 
          'title': self._title 
      }
      print ("Creating tasklist: " + self._title)
      tasklists.insert(body=_body).execute()
      self._tasklist = tasklists.list(tasklist=self._title)

    
  def CreateIfNotExists (self, title):
    try:
      result = GoogleAuth.getService(self).tasklists().list().execute()
      for item in result["items"]:
        if (item["title"] == title):
          self._tasklist = item
          print (" ** " + self._tasklist["title"] + " >> " + self._tasklist["id"])
        else: 
          print ("    " + item["title"])

      if not self._tasklist:
          print ("Creating: " + self._title)
          _body = { 
              'title': self._title 
          }
          self._tasklist = GoogleAuth.getService(self).tasklists().insert(body=_body).execute()

    except AccessTokenRefreshError:
      print ("The credentials have been revoked or expired, please re-run"
        "the application to re-authorize")
    pass

  def AddTask (self, task):
    print ("Adding :" + task._title)
    try:
      GoogleAuth.getService(self).tasks().insert(tasklist=self._tasklist['id'], body=task.getBody()).execute()
    except:
      pass

  def List(self):
    print ("Task List:" + self._tasklist['title'] + " >> " + self._tasklist['id'] )
    try:
      result = GoogleAuth.getService(self).tasks().list(tasklist=self._tasklist['id']).execute()
      for item in result["items"]:
        print (" Task found: " + item["title"] + " >> " + item['id'])
    except:
      pass

  def Delete (self):
    try:
      result = GoogleAuth.getService(self).tasklists().delete(tasklist=self._tasklist['id']).execute()
      print ("Deleting " + self._tasklist['title'] + " : SUCCESS")
      self._tasklist = None
    except:
      print ("Deleting " + self._tasklist['title'] + " : FAIL")
      pass
    pass


def main (argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)


  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))


  tlist = TaskList("MyTestList")
  tlist.List()
  sofia = Task("Sofia")
  ella = Task("ella")

  tlist.AddTask(sofia)
  tlist.AddTask(ella)
  tlist.List()
  tlist.Delete()





if __name__ == '__main__':
  main(sys.argv)

