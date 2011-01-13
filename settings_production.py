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
