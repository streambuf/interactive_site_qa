import os
import sys	
sys.path.append('/home/max/askmoiseev/askmoiseev')
os.environ['DJANGO_SETTINGS_MODULE'] = 'askmoiseev.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()