import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'crust.settings'
sys.path.append('/home/vagrant/src/www/')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
