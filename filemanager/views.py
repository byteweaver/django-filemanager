import json
import os

from django.views.generic import TemplateView, FormView
from django.views.generic.base import View
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse_lazy
from django.core.files.base import ContentFile

from filemanager.forms import DirectoryCreateForm
from filemanager.settings import MEDIA_ROOT, MEDIA_URL, STORAGE
from filemanager.utils import sizeof_fmt
from filemanager.core import Filemanager


def get_abspath(relpath):
    return os.path.join(MEDIA_ROOT, relpath)

def get_absurl(relurl):
    return os.path.join(MEDIA_URL, relurl)


class FilemanagerMixin(object):
    def __init__(self, *args, **kwargs):

        self.storage = STORAGE

        return super(FilemanagerMixin, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(FilemanagerMixin, self).get_context_data(*args, **kwargs)

        self.fm = Filemanager(self.get_relpath())
        self.fm.patch_context_data(context)

        return context

    def get_relpath(self):
        if 'path' in self.request.GET and len(self.request.GET['path']) > 0:
            return os.path.relpath(self.request.GET['path'])
        if 'path' in self.request.POST and len(self.request.POST['path']) > 0:
            return os.path.relpath(self.request.POST['path'])
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
            'filedate': self.storage.modified_time(abspath),
            'fileurl': self.storage.url(get_absurl(path)),
        }

        return context


class UploadView(FilemanagerMixin, TemplateView):
    template_name = 'filemanager/filemanager_upload.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UploadView, self).get_context_data(*args, **kwargs)

        # add an upload entry to the end of our breadcrumbs list
        context['breadcrumbs'].append({
            'path': '#',
            'label': 'Upload'
        })

        return context


class UploadFileView(FilemanagerMixin, View):
    def post(self, request, *args, **kwargs):
        if len(request.FILES) != 1:
            return HttpResponseBadRequest("Just a single file please.")

        filedata = request.FILES['files[]']

        filepath = os.path.join(self.get_relpath(), self.storage.get_valid_name(filedata.name))

        # TODO: get filepath and validate characters in name, validate mime type and extension

        self.storage.save(filepath, filedata)

        return HttpResponse(json.dumps({
            'files': [{'name': filedata.name}],
        }))


class DirectoryCreateView(FilemanagerMixin, FormView):
    template_name = 'filemanager/filemanager_create_directory.html'
    form_class = DirectoryCreateForm

    def get_success_url(self):
        return reverse_lazy('filemanager:browser') + '?path=' + self.get_relpath()

    def form_valid(self, form):
        directory_name = self.storage.get_valid_name(form.cleaned_data.get('directory_name'))

        directory_path = os.path.join(directory_name, '.tmp')

        path = os.path.join(self.get_relpath(), directory_path)

        self.storage.save(path, ContentFile(''))
        self.storage.delete(path)

        return super(DirectoryCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(DirectoryCreateView, self).get_context_data(*args, **kwargs)

        # add an upload entry to the end of our breadcrumbs list
        context['breadcrumbs'].append({
            'path': '#',
            'label': 'Create directory'
        })

        return context
