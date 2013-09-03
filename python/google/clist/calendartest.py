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
  service_list = {"items":[
    {
      "name": "tasks",
      "version": "v1",
      "storage_file": "tasks.dat",
      "store": None
    },
    {
      "name": "calendar",
      "version": "v3",
      "storage_file": "calendar.dat",
      "store": None
    }
  ]
  }
  def __init__(self):
    self.task_service = None
    self.calendar_service = None
    for service in self.service_list['items']:
      task_storage = Storage(service['storage_file'])
      credentials = task_storage.get()

      if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, task_storage)

      http = httplib2.Http()
      http = credentials.authorize(http)

      service['store']     = build(serviceName=service['name'], version=service['version'], http=http, developerKey='')

    calendar_service = self.service_list['items'][1]['store']
    calendar_list_entry = {
        'id': 'calendarId'
    }

    created_calendar_list_entry = service.calendarList().insert(body=calendar_list_entry).execute()

    print created_calendar_list_entry['summary']

  def get_task_service(self):
    return self.service_list['items'][0]['store']
      
  def get_calendar_service(self):
    return self.service_list['items'][1]['store']
