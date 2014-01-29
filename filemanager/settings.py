import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


DIRECTORY = getattr(settings, 'FILEMANAGER_DIRECTORY', 'uploads')

MEDIA_ROOT = getattr(settings, "FILEMANAGER_MEDIA_ROOT", os.path.join(settings.MEDIA_ROOT, DIRECTORY))

MEDIA_URL = getattr(settings, "FILEMANAGER_MEDIA_URL", os.path.join(settings.MEDIA_URL, DIRECTORY))

STORAGE = getattr(settings, "FILEMANAGER_STORAGE", FileSystemStorage(location=MEDIA_ROOT, base_url=MEDIA_URL))
