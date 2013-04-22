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



CLIENT_SECRETS = 'crustifier.json'
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to download the client_secrets.json file
and save it at

   %s

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

FLOW = OAuth2WebServerFlow(
    client_id="838345617067.apps.googleusercontent.com", 
    client_secret="rpL19YcdHDCr1gbuod8eN7CZ",
    scope= 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/tasks',
    user_agent="crustifier/V0.1")


class GoogleService:
  def __init__(self):
    task_storage = Storage('tasks.dat')
    credentials = task_storage.get()

    if credentials is None or credentials.invalid == True:
      credentials = run(FLOW, task_storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    self.task_service     = build(serviceName='tasks', version='v1', http=http, developerKey='')

    calendar_storage = Storage('calendar.dat')
    credentials = calendar_storage.get()

    if credentials is None or credentials.invalid == True:
      credentials = run(FLOW, calendar_storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    self.calendar_service = build(serviceName='calendar', version='v3', http=http, developerKey='')

  def get_task_service(self):
    return self.task_service
      
  def get_calendar_service(self):
    return self.calendar_service
