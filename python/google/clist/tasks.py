"""
https://developers.google.com/google-apps/tasks/v1/reference/tasks#resource

{
  "kind": "tasks#task",
  "id": string,
  "etag": etag,
  "title": string,
  "updated": datetime,
  "selfLink": string,
  "parent": string,
  "position": string,
  "notes": string,
  "status": string,
  "due": datetime,
  "completed": datetime,
  "deleted": boolean,
  "hidden": boolean,
  "links": [
    {
      "type": string,
      "description": string,
      "link": string
    }
  ]
}
"""
class Task:
  def __init__(self, taskfd, id):
    self.taskfd = taskfd
    self.tasklist_id = id
    pass

  def list(self):
    pass

  def insert(self):
    task = {
      'title': 'New Task',
      'notes': 'Please complete me',
      'due': '2010-10-15T12:00:00.000Z'
    }
    
    result = self.taskfd.insert(tasklist=self.tasklist_id, body=task).execute()
    
