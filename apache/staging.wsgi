import os, sys, site

sys.path.append('/var/www/diabeaters/diabeaters/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'diabeaters.settings_staging'

import django.core.handlers.wsgi

import django
django.setup()

application = django.core.handlers.wsgi.WSGIHandler()
