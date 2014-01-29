import os

from django.conf import settings
from django.core.files.base import ContentFile

from filemanager.settings import DIRECTORY, STORAGE
from filemanager.utils import sizeof_fmt


class Filemanager(object):
    def __init__(self, path=None):
        self.update_path(path)

    def update_path(self, path):
        if path is None or len(path) == 0:
            self.path = ''
            self.abspath = DIRECTORY
        else:
            self.path = self.validate_path(path)
            self.abspath = os.path.join(DIRECTORY, self.path)
        self.location = os.path.join(settings.MEDIA_ROOT, self.abspath)
        self.url = os.path.join(settings.MEDIA_URL, self.abspath)

    def validate_path(self, path):
        # replace backslash with slash
        path = path.replace('\\', '/')
        # remove leading and trailing slashes
        path = '/'.join([i for i in path.split('/') if i])

        return path

    def get_breadcrumbs(self):
        breadcrumbs = [{
            'label': 'Filemanager',
            'path': '',
        }]

        parts = [e for e in self.path.split('/') if e]

        path = ''
        for part in parts:
            path = os.path.join(path, part)
            breadcrumbs.append({
                'label': part,
                'path': path,
            })

        return breadcrumbs

    def patch_context_data(self, context):
        context.update({
            'path': self.path,
            'breadcrumbs': self.get_breadcrumbs(),
        })

    def file_details(self):
        filepath, filename = self.path.rsplit('/', 1)
        return {
            'filepath': filepath,
            'filename': filename,
            'filesize': sizeof_fmt(STORAGE.size(self.location)),
            'filedate': STORAGE.modified_time(self.location),
            'fileurl': self.url,
        }

    def directory_list(self):
        listing = []

        directories, files = STORAGE.listdir(self.location)

        def _helper(name, filetype):
            return {
                'filepath': os.path.join(self.path, name),
                'filetype': filetype,
                'filename': name,
                'filedate': STORAGE.modified_time(os.path.join(self.path, name)),
                'filesize': sizeof_fmt(STORAGE.size(os.path.join(self.path, name))),
            }

        for directoryname in directories:
            listing.append(_helper(directoryname, 'Directory'))

        for filename in files:
            listing.append(_helper(filename, 'File'))

        return listing

    def upload_file(self, filedata):
        filename = STORAGE.get_valid_name(filedata.name)
        STORAGE.save(os.path.join(self.path, filename), filedata)
        return filename

    def create_directory(self, name):
        name = STORAGE.get_valid_name(name)
        tmpfile = os.path.join(name, '.tmp')

        path = os.path.join(self.path, tmpfile)

        STORAGE.save(path, ContentFile(''))
        STORAGE.delete(path)
