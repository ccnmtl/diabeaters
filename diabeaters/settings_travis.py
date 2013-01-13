from settings_shared import *

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'diabeaters',
        'HOST' : '127.0.0.1',
        'PORT' : 5432,
        'USER' : 'postgres',
        'PASSWORD' : '',
        }
}

STATSD_HOST = '127.0.0.1'

try:
    from local_settings import *
except ImportError:
    pass
