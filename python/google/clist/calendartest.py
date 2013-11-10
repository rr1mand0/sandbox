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

import httplib2
import os
import pprint
import sys
import json

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


FLOW = OAuth2WebServerFlow(
    client_id="838345617067.apps.googleusercontent.com", 
    client_secret="rpL19YcdHDCr1gbuod8eN7CZ",
    scope= 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/tasks',
    user_agent="crustifier/V0.1")


class GoogleService:
  service_list = {
    "tasks": {
      "name": "tasks",
      "version": "v1",
      "storage_file": "tasks.dat",
      "store": None
    },
    'calendar': {
      "name": "calendar",
      "version": "v3",
      "storage_file": "calendar.dat",
      "store": None
    }
  }
  def _init_service(self, name):
    task_storage = Storage(self.service_list[name]['storage_file'])
    credentials = task_storage.get()

    print ('Initializing: %s' % json.dumps(self.service_list[name]))
    if credentials is None or credentials.invalid == True:
      credentials = run(FLOW, task_storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    version = self.service_list[name]['version']
    service = build(serviceName=self.service_list[name]['name'], 
        version=version, http=http, developerKey='')

    self.service_list[name]['store'] = service

  def get_store(self, name):
    return self.service_list[name]['store']

  def __init__(self):
    self.task_service = None
    self.calendar_service = None
    for name, value in self.service_list.items():
      self._init_service(name)

  def get_calendar_list(self):
    page_token = None
    while True:
      calendar_list = self.get_store('calendar').calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        print calendar_list_entry['summary']
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break

  def get_task_service(self):
    return self.get_store('task')
      
  def get_calendar_service(self):
    return self.get_store('calendar')

GoogleService()
