from googleservice import GoogleService
from tasklist import TaskList
from oauth2client.client import AccessTokenRefreshError
import logging
import sys
import gflags

FLAGS = gflags.FLAGS
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')

def main(argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  service = GoogleService().get_service()

  try:

    print "Success! Now add code here."
    tl = service.tasklists()
    tasklist = {
      'title': "test list"
    }
    
    t = TaskList(tl, "rays-test=00")
    t.Insert()
    t.Delete()

    #calService = build(serviceName='calendar', version='v3', http=http)
    #cal = Calendar(calService)
    #cal.List()

  except AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
