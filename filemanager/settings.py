import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


MEDIA_ROOT = getattr(settings, "FILEMANAGER_MEDIA_ROOT", os.path.join(settings.MEDIA_ROOT, 'uploads'))

MEDIA_URL = getattr(settings, "FILEMANAGER_MEDIA_URL", os.path.join(settings.MEDIA_URL, 'uploads'))

STORAGE = getattr(settings, "FILEMANAGER_STORAGE", FileSystemStorage(location=MEDIA_ROOT, base_url=MEDIA_URL))
