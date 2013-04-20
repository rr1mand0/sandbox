# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for Tasks API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

To get detailed log output run:

  $ python sample.py --logging_level=DEBUG
"""

import gflags
import httplib2
import logging
import os
import pprint
import sys
import json
#import Task

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


FLAGS = gflags.FLAGS

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret.
# You can see the Client ID and Client secret on the API Access tab on the
# Google APIs Console <https://code.google.com/apis/console>
CLIENT_SECRETS = 'client_secrets.json'

# Helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to download the client_secrets.json file
and save it at:

   %s

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
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


class TaskList:
  tasklist = {}

  def __init__ (self, tasklist, title):
    self.servicetasklist = tasklist
    self.title = title

  def GetId(self):
    result = self.servicetasklist.list().execute()
    i=0
    while (1):
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
      id = self.GetId()
      self.servicetasklist.delete(tasklist=id).execute()

    
def main(argv):
  # Let the gflags module process the command-line arguments
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  storage = Storage('sample.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage)

  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build('tasks', 'v1', http=http)

  try:

    print "Success! Now add code here."
    tl = service.tasklists()
    tasklist = {
      'title': "test list"
    }
    
    #tl.insert(body=tasklist).execute()
    t = TaskList(tl, "rays-test=00")
    t.Insert()
    t.Delete()

    #result = tl.list().execute()
    #print json.dumps(result, indent=2, separators=(',', ': '))
  except AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

#json.dumps([1,2,3,{'4': 5, '6': 7}], separators=(',',':'))
if __name__ == '__main__':
  main(sys.argv)
