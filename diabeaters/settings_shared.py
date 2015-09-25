# Django settings for diabeaters project.
import os.path
from ccnmtlsettings.shared import common

project = 'diabeaters'
base = os.path.dirname(__file__)

locals().update(
    common(
        project=project,
        base=base,
    ))

PROJECT_APPS = [
    'diabeaters.main',
    'diabeaters.quiz',
    'diabeaters.healthhabitplan',
]

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'pagetree',
    'pageblocks',
    'diabeaters.quiz',
    'diabeaters.main',
    'diabeaters.healthhabitplan',
]

PAGEBLOCKS = ['pageblocks.TextBlock',
              'quiz.Quiz',
              'pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'pageblocks.ImageBlock',
              'pageblocks.ImagePullQuoteBlock']

THUMBNAIL_SUBDIR = "thumbs"

AUTH_PROFILE_MODULE = "main.UserProfile"
