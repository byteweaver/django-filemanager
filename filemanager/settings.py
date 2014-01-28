import os

from django.conf import settings


MEDIA_ROOT = getattr(settings, "FILEMANAGER_MEDIA_ROOT", os.path.join(settings.MEDIA_ROOT, 'uploads'))
