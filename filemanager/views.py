import os

from django.views.generic import TemplateView

from filemanager.settings import MEDIA_ROOT, STORAGE
from filemanager.utils import sizeof_fmt, generate_breadcrumbs


def get_abspath(relpath):
    return os.path.join(MEDIA_ROOT, relpath)


class FilemanagerMixin(object):
    def __init__(self, *args, **kwargs):

        self.storage = STORAGE

        return super(FilemanagerMixin, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(FilemanagerMixin, self).get_context_data(*args, **kwargs)

        context['path'] = self.get_relpath()

        context['breadcrumbs'] = [{
            'label': 'Filemanager',
            'url': '',
        }] + generate_breadcrumbs(self.get_relpath())

        return context

    def get_relpath(self):
        if 'path' in self.request.GET and len(self.request.GET['path']) > 0:
            return os.path.relpath(self.request.GET['path'])
        return ''


class BrowserView(FilemanagerMixin, TemplateView):
    template_name = 'filemanager/browser/filemanager_list.html'

    def get_context_data(self, **kwargs):
        context = super(BrowserView, self).get_context_data(**kwargs)

        path = self.get_relpath()

        context['files'] = []

        browse_path = os.path.join(MEDIA_ROOT, path)

        directories, files = self.storage.listdir(browse_path)

        for directoryname in directories:
            path = get_abspath(os.path.join(browse_path, directoryname))
            context['files'].append({
                'filepath': os.path.join(self.get_relpath(), directoryname),
                'filetype': 'Directory',
                'filename': directoryname,
                'filesize': '-',
                'filedate': self.storage.modified_time(path)
            })

        for filename in files:
            path = get_abspath(os.path.join(browse_path, filename))
            context['files'].append({
                'filepath': os.path.join(self.get_relpath(), filename),
                'filetype': 'File',
                'filename': filename,
                'filesize': sizeof_fmt(self.storage.size(path)),
                'filedate': self.storage.modified_time(path)
            })

        return context


class DetailView(FilemanagerMixin, TemplateView):
    template_name = 'filemanager/browser/filemanager_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        path = self.get_relpath()
        filename = path.rsplit('/', 1)[-1]
        abspath = get_abspath(path)

        context['file'] = {
            'filepath': path[:-len(filename)],
            'filename': filename,
            'filesize': sizeof_fmt(self.storage.size(abspath)),
            'filedate': self.storage.modified_time(abspath)
        }

        return context


class UploadView(FilemanagerMixin, TemplateView):
    template_name = 'filemanager/filemanager_upload.html'
