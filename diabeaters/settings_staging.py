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
        }
}

SENTRY_SITE = 'diabeaters-staging'
STATSD_PREFIX = 'diabeaters-staging'

if 'migrate' not in sys.argv:
    import logging
    from raven.contrib.django.handlers import SentryHandler
    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
