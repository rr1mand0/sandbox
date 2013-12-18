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


class GoogleService(object):
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
    print ("initialized %s" % name)

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
    return self.get_store('tasks')
      
  def get_calendar_service(self):
    return self.get_store('calendar')

  def get_calendar_by_name(self, name):
    cal = self.get_calendar_service()
    cal_list = cal.calendarList().list().execute()

    for item in cal_list['items']:
      if item['summary'] == name:
        return item
    return None

  def get_calendar_id_by_name(self, name):
    calendar = self.get_calendar_by_name(name)
    if calendar:
      return calendar['id']
    return None

  def get_calendar_dict_from_name(self, name):
    id = self.get_calendar_id_by_name (name)
    print ("id: %s" % id)
    if id:
      return self.get_calendar_service().calendars().get(calendarId=id).execute()
    return None

  def get_calendar_events(self, name):
    id = self.get_calendar_id_by_name (name)
    if id:
      page_token = None
      all_events = []
      while True:
        events = self.get_calendar_service().events().list(calendarId=id, pageToken=page_token).execute()
        all_events = all_events + events['items']
        print ("received %d events %d" % (events['items'].__len__(), all_events.__len__()))
        
        page_token = events.get('nextPageToken')
        if not page_token:
          break
      print ("returning %d items" % all_events.__len__())
      return all_events
    return None

  def import_events_to_couchdb(self, server, name):
    import couchdb
    couch = couchdb.Server(server)
    print ('Creating db:%s on server:%s' %(name, server))

    # try and create a database
    try:
      db = couch.create(name.lower()) 
    except couchdb.http.PreconditionFailed:
      pass
    db = couch[name.lower()]

    events = self.get_calendar_events(name)

    for event in events:
      print event
      db.save(event)

    fd = open ("events.json", 'w')
    fd.write(json.dumps({'items':events}, indent=2))
    fd.close()
    
