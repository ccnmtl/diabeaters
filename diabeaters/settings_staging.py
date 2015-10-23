# flake8: noqa
from settings_shared import *
from ccnmtlsettings.staging import common

locals().update(
    common(
        project=project,
        base=base,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
        cloudfront="d2pl7wm2o23pxj",
    ))

try:
    from local_settings import *
except ImportError:
    pass
