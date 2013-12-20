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

import logging
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
  task = None
  calendar = None

  @staticmethod
  def _init_service(gservice):
    logging.info ('Initializing: %s' % json.dumps(gservice, indent=2))
    task_storage = Storage(gservice['storage_file'])
    credentials = task_storage.get()

    if credentials is None or credentials.invalid == True:
      credentials = run(FLOW, task_storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    version = gservice['version']
    service = build(serviceName=gservice['name'], 
        version=version, http=http, developerKey='')

    gservice['store'] = service
    logging.debug ("initialized %s" % gservice['name'])
    return service

  @classmethod
  def get_tasks(cls):
    task_service = {
      'name': 'tasks',
      'version': 'v1',
      'storage_file': 'tasks.dat',
      'store': None
    }
    if not cls.task:
      cls.task = cls._init_service(task_service)
    return cls.task 

  @classmethod
  def get_calendar(cls):
    calendar_service = {
      'name': 'calendar',
      'version': 'v3',
      'storage_file': 'calendar.dat',
      'store': None
    }
    if not cls.calendar:
      cls.calendar = cls._init_service(calendar_service)
    return cls.calendar 

  def get_store(self):
    return service_list['store']

  def __init__(self, service_list):
    self._init_service(service_list)
    self.task_service = None
    self.calendar_service = None

  def get_task_service(self):
    return self.get_store('tasks')
      
  def get_calendar_service(self):
    return self.get_store('calendar')


  def get_calendar_events(self, name):
    id = self.get_calendar_id_by_name (name)
    if id:
      page_token = None
      all_events = []
      while True:
        events = self.get_calendar_service().events().list(calendarId=id, pageToken=page_token).execute()
        all_events = all_events + events['items']
        logging.debug ("received %d events %d" % (events['items'].__len__(), all_events.__len__()))
        
        page_token = events.get('nextPageToken')
        if not page_token:
          break
      logging.debug ("returning %d items" % all_events.__len__())
      return all_events
    return None

  def import_events_to_couchdb(self, server, name):
    import couchdb
    couch = couchdb.Server(server)
    logging.debug ('Creating db:%s on server:%s' %(name, server))

    # try and create a database
    try:
      db = couch.create(name.lower()) 
    except couchdb.http.PreconditionFailed:
      pass
    db = couch[name.lower()]

    events = self.get_calendar_events(name)

    for event in events:
      logging.debug ('%s' % event)
      db.save(event)

    fd = open ("events.json", 'w')
    fd.write(json.dumps({'items':events}, indent=2))
    fd.close()
    
class GCalendarList(GoogleService):
  def __init__(self):
    self.calendar = GoogleService.get_calendar()

  def get_calendarList_item_by_name(self, name):
    calendarlist = self.get_calendar_list()
    for calendarListItem in calendarlist:
      if calendarListItem['summary'] == name:
        return calendarListItem
    return {}

  def exists(self, name):
    if self.get_calendarList_item_by_name(name):
      return True
    return False

  def create(self, calendarList_name):
    _item = self.get_calendarList_item_by_name(calendarList_name)
    if not _item:
      _item = self.calendar.calendarList().insert(body={'id': calendarList_name}).execute()
    return _item

  def get_calendar_list(self):
    page_token = None
    while True:
      calendar_list = self.calendar.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        logging.debug ('get_calendar_list: %s' % (calendar_list_entry['summary']))
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    return calendar_list['items']

  def get_calendar_by_name(self, name):
    cal_list = self.calendar.calendarList().list().execute()

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
    logging.debug ("id: %s" % id)
    if id:
      return self.calendar.calendars().get(calendarId=id).execute()
    return None

class GTask(GoogleService):
  def __init__(self, id = None):
    self.task = GoogleService.get_tasks()
    self.id = id
    logging.debug ("Task: %s" % self.list())

  def insert(self, task):
    self.task.tasks().insert(tasklist=self.id, body=task).execute()

  def list(self):
    tasks = self.task.tasks().list(tasklist=self.id).execute()
    if tasks.has_key('items'):
      return tasks['items']
    return {}

  def get_by_title(self, title):
    for task in self.list():
      if task['title'] == title:
        return task
    return {}

  def delete_by_title(self, title):
    taskid = self.get_by_title(title)
    if taskid:
      rc = self.task.tasks().delete(tasklist=self.id, task=taskid['id']).execute()
      logging.debug ('[%s] deleting task id:%s title:\'%s\'' %
          (rc, taskid['id'], taskid['title']))

  def __len__(self):
    items = self.list()
    return items.__len__()


class GTaskList(GoogleService):
  def __init__(self):
    self.tasks = GoogleService.get_tasks()

  def create(self, tasklist):
    _list = self.get_list_by_name(tasklist['title'])
    if not _list:
      _list = self.tasks.tasklists().insert(body=tasklist).execute()
    return _list

  def delete(self, listname):
    tasklist = self.get_list_by_name(listname)
    if tasklist:
      logging.debug ('Deleting tasklist with id=%s\n%s' % (tasklist['id'], json.dumps(tasklist, indent=2)))
      return self.tasks.tasklists().delete(tasklist=tasklist['id']).execute()

  def get_tasklist(self):
    return self.tasks.tasklists().list().execute()['items']
    #tasklist =  self.tasks.tasklists().list().execute()
    #if tasklist.has_key('items'):
      #return tasklist['items']
    #return {}

  def get_list_by_name(self, name):
    lists = self.get_tasklist()
    for _list in lists:
      logging.debug ("get_list_by_name: %s == %s" % (name, _list['title']))
      if _list['title'] == name:
        return _list
    return {}

      
  def exists(self, listname):
    if self.get_list_by_name(listname):
      logging.debug ('exists: found %s' % listname)
      return True
    return False

  def create_task_list(self, name):
    pass

