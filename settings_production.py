from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/diabeaters/diabeaters/templates",
)

MEDIA_ROOT = '/var/www/diabeaters/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/diabeaters/diabeaters/sitemedia'),	
)


DEBUG = False
TEMPLATE_DEBUG = True
SENTRY_SITE = "diabeaters"

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'diabeaters',
        'HOST' : '',
        'PORT' : 5432,
        'USER' : '',
        'PASSWORD' : '',
        }
}

try:
    from local_settings import *
except ImportError:
    pass
