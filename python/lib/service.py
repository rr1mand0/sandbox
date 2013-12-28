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

class Singleton(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]


class GoogleService(object):

  _gservice = None
  def __init__(self, google_dict, label = 'title'):
    self.label = label
    task_storage = Storage(google_dict['storage_file'])
    credentials = task_storage.get()

    if credentials is None or credentials.invalid == True:
      credentials = run(FLOW, task_storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    version = google_dict['version']
    self._gservice = build(serviceName=google_dict['name'], 
        version=version, http=http, developerKey='')

    google_dict['store'] = self._gservice
    logging.debug ("initialized %s" % google_dict['name'])


  def exists(self, item_name):
    if self.get_item_by_name(item_name):
      logging.debug ('exists: found %s' % item_name)
      return True
    return False

  def delete(self, item_name):
    self.get_item_by_name(item)

  def get_items(self):
    items =  self._function.list().execute()
    if items.has_key('items'):
      return items['items']
    return {}

  def get_item_by_name(self, name):
    items = self.get_items()
    for item in items:
      if item[self.label] == name:
        return item
    return {}

  def __len__(self):
    return self.get_items().__len__()
    
class GCalendarWrapper(GoogleService, Singleton):
  cal_dict = {
    'name': 'calendar',
    'version': 'v3',
    'storage_file': 'calendar.dat',
    'store': None
  }
  #_gservice = None
  def __init__(self, title=None):
    if not self._gservice:
      self.cal_dict['title'] = title
      GoogleService.__init__(self, self.cal_dict, label='summary')
      self.cal_dict['store'] = self._gservice 

class GCalendar(GCalendarWrapper):
  def __init__(self, name):
    GCalendarWrapper.__init__(self, name)
    self._function = self._gservice.calendars()
    self._events = self._gservice.events()
    self.calendarListFd = GCalendarList()

    # initialize the calendar
    self.calendar = self.calendarListFd.get_item_by_name(name)
    if not self.calendar:
      self.calendar = self._function.insert(body={'summary': name}).execute()

  def insert_event(self, event):
    return self._events.insert(calendarId=self.calendar['id'], body=event).execute()

  def get_events(self, start_date=None, end_date=None):
    events = self._events.list(calendarId=self.calendar['id'], timeMin=start_date, timeMax=end_date).execute()['items']
    logging.debug('get_events:\n %s' % json.dumps(events, indent=2))
    return events

  def delete_events(self, start_date=None, end_date=None):
    events = self.get_events(start_date=start_date, end_date=end_date)
    for event in events:
      logging.debug('deleting event: %s %s' % (event['id'], event['summary']))
      self._events.delete(calendarId=self.calendar['id'], eventId=event['id']).execute()

  def push_events_to_tasks(self, tasklist_name, start_date=None, end_date=None):
    taskfd = GTask(tasklist_name)

    # push the meals into the tasklist
    events = self.get_events(start_date=start_date, end_date=end_date)
    for event in events:
      new_task = {
        'title': event['summary']
      }
      logging.debug('adding event to task: \n%s' % (json.dumps(new_task, indent=2)))
      taskfd.insert(new_task)
  
class GEvents(GCalendarWrapper):
  def __init__(self, calendarId):
    GCalendarWrapper.__init__(self)
    self._function = self._gservice.events()
    self.id = calendarId

  def insert(self, event):
    return self._function.insert(event).execute()


class GCalendarList(GCalendarWrapper):
  def __init__(self):
    GCalendarWrapper.__init__(self)
    self._function = self._gservice.calendarList()

  def delete(self, name):
    _item = self.get_item_by_name(name)
    if _item:
      self._function.delete(calendarId = _item['id']).execute()

  def get_calendar_events(self, name):
    id = self.get_item_by_name (name)
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

class GTaskWrapper(GoogleService):
  task_dict = {
    'name': 'tasks',
    'version': 'v1',
    'storage_file': 'tasks.dat',
    'store': None
  }
  #_gservice = None
  def __init__(self, title=None):
    if not self._gservice:
      logging.debug('initializing tasks service')
      self.task_dict['title'] = title
      GoogleService.__init__(self, self.task_dict)
      self.task_dict['store'] = self._gservice 

class GTask(GTaskWrapper):
  def __init__(self, tasklist_name):
    GTaskWrapper.__init__(self, tasklist_name)

    tasklistFd = GTaskList()
    self.tasklist = tasklistFd.get_item_by_name(tasklist_name)
    if not self.tasklist:
      self.tasklist = tasklistFd.insert({'title': tasklist_name})

    self.id = self.tasklist['id']
    self._function = self._gservice.tasks()

  def insert(self, task, parent=None):
    """ 
    override 
    """
    return self._function.insert(tasklist=self.id, body=task, parent=parent).execute()

  def get_items(self):
    """ 
    override 
    """
    items = self._function.list(tasklist=self.id).execute()
    if items.has_key('items'):
      return items['items']
    return {}

  def delete_by_id(self, id):
    logging.debug ('deleting task id:%s ' % (id))
    return self._function.delete(tasklist=self.id, task=id).execute()

  def delete(self, name):
    taskid = self.get_item_by_name(name)
    if taskid:
      rc = self.delete_by_id(taskid['id'])

  def clear(self):
    items = self.get_items()
    for item in items:
      rc = self.delete_by_id(item['id'])

class GTaskList(GTaskWrapper):
  def __init__(self):
    GTaskWrapper.__init__(self, title=None)
    self._function = self._gservice.tasklists()

  def insert(self, tasklist):
    _list = self.get_item_by_name(tasklist[self.label])
    if not _list:
      _list = self._gservice.tasklists().insert(body=tasklist).execute()
    return _list

  def delete(self, name):
    item = self.get_item_by_name(name)
    if item:
      return self._function.delete(tasklist=item['id']).execute()


import couch
class ShoppingGenerator(object):
  def __init__(self, calendarName, taskName, server, dbname):
    self.calendarName = calendarName
    self.taskName = taskName

    self.calFd = GCalendar(calendarName)
    self.taskFd = GTask(taskName)

    self.recipedb = couch.Recipes(server=server, dbname=dbname)

  def publish(self, start_date, end_date):
    events = self.calFd.get_events(start_date=start_date, end_date=end_date)
    # push the meals into the tasklist
    for event in events:
      print ("Publishing: %s: %s" % (event['start']['date'], event['summary']))
      logging.debug ("publishing: %s" % event)
      self.recipedb.export_to_gtask(event['summary'], self.taskName)


