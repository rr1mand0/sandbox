# -*- coding: utf-8 -*-

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

  def getService(self):
    return self.service

class Item(object):
  def __init__(self, name):
    pass

class TaskList(GoogleAuth):
  def __init__(self, name):
    self.name = name

    # authenticate 
    GoogleAuth.__init__(self)
    try:
      print "Success! Now add code here."
      result = GoogleAuth.getService(self).tasklists().list().execute()
      print (result["items"][0]["title"])
      for item in result["items"]:
        #print ("item found: " + item["title"] + " :: " + name)
        if (item["title"] == name):
          print ("List found: " + item["title"])
          self.list = item
    except AccessTokenRefreshError:
      print ("The credentials have been revoked or expired, please re-run"
        "the application to re-authorize")
    pass

  def Create (self):
    pass

  def AddItem (self, item):
    pass

  def Delete (self):
    pass

  def List(self,id):
    pass



def main (argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  s = TaskList("Raymund's list")
  s.List(0)

if __name__ == '__main__':
  main(sys.argv)
