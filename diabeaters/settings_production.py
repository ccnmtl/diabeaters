# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/diabeaters/diabeaters/diabeaters/templates",
)

MEDIA_ROOT = '/var/www/diabeaters/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/diabeaters/diabeaters/sitemedia'),
)


DEBUG = False
TEMPLATE_DEBUG = True

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'diabeaters',
        'HOST' : '',
        'PORT' : 6432,
        'USER' : '',
        'PASSWORD' : '',
        'ATOMIC_REQUEST': True,
        }
}

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
