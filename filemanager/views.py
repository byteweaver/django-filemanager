import os

from django.core.files.storage import DefaultStorage
from django.views.generic import TemplateView

from filemanager.settings import MEDIA_ROOT
from filemanager.utils import sizeof_fmt, generate_breadcrumbs


def get_abspath(relpath):
    return os.path.join(MEDIA_ROOT, relpath)


class BrowserView(TemplateView):
    template_name = 'filemanager/browser/filemanager_list.html'

    def get_relpath(self):
        if 'path' in self.request.GET:
            return self.request.GET['path']
        return ''

    def get_context_data(self, **kwargs):
        context = super(BrowserView, self).get_context_data(**kwargs)

        storage = DefaultStorage()

        path = self.get_relpath()

        context['breadcrumbs'] = [{
            'label': 'Filemanager',
            'url': '',
        }] + generate_breadcrumbs(path)

        context['files'] = []

        browse_path = os.path.join(MEDIA_ROOT, path)

        directories, files = storage.listdir(browse_path)

        for directoryname in directories:
            path = get_abspath(os.path.join(browse_path, directoryname))
            context['files'].append({
                'filepath': os.path.join(self.get_relpath(), directoryname),
                'filetype': 'Directory',
                'filename': directoryname,
                'filesize': '-',
                'filedate': storage.modified_time(path)
            })

        for filename in files:
            path = get_abspath(os.path.join(browse_path, filename))
            context['files'].append({
                'filepath': os.path.join(self.get_relpath(), filename),
                'filetype': 'File',
                'filename': filename,
                'filesize': sizeof_fmt(storage.size(path)),
                'filedate': storage.modified_time(path)
            })

        return context
