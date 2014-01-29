import json
import os

from django.views.generic import TemplateView, FormView
from django.views.generic.base import View
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse_lazy

from filemanager.forms import DirectoryCreateForm
from filemanager.settings import STORAGE
from filemanager.utils import sizeof_fmt
from filemanager.core import Filemanager


class FilemanagerMixin(object):
    def __init__(self, *args, **kwargs):

        self.storage = STORAGE

        return super(FilemanagerMixin, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        params = dict(request.GET)
        params.update(dict(request.POST))

        self.fm = Filemanager()
        if 'path' in params and len(params['path'][0]) > 0:
            self.fm.update_path(params['path'][0])

        return super(FilemanagerMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(FilemanagerMixin, self).get_context_data(*args, **kwargs)

        self.fm.patch_context_data(context)

        if hasattr(self, 'extra_breadcrumbs') and isinstance(self.extra_breadcrumbs, list):
            context['breadcrumbs'] += self.extra_breadcrumbs

        return context


class BrowserView(FilemanagerMixin, TemplateView):
    template_name = 'filemanager/browser/filemanager_list.html'

    def get_context_data(self, **kwargs):
        context = super(BrowserView, self).get_context_data(**kwargs)

        context['files'] = []

        directories, files = self.storage.listdir(self.fm.location)

        for directoryname in directories:
            context['files'].append({
                'filepath': os.path.join(self.fm.path, directoryname),
                'filetype': 'Directory',
                'filename': directoryname,
                'filesize': '-',
                'filedate': self.storage.modified_time(os.path.join(self.fm.location, directoryname))
            })

        for filename in files:
            abspath = os.path.join(self.fm.location, filename)
            context['files'].append({
                'filepath': os.path.join(self.fm.path, filename),
                'filetype': 'File',
                'filename': filename,
                'filesize': sizeof_fmt(self.storage.size(abspath)),
                'filedate': self.storage.modified_time(abspath)
            })

        return context


class DetailView(FilemanagerMixin, TemplateView):
    template_name = 'filemanager/browser/filemanager_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        filename = self.fm.path.rsplit('/', 1)[-1]

        context['file'] = {
            'filepath': self.fm.path[:-len(filename)],
            'filename': filename,
            'filesize': sizeof_fmt(self.storage.size(self.fm.location)),
            'filedate': self.storage.modified_time(self.fm.location),
            'fileurl': self.fm.url,
        }

        return context


class UploadView(FilemanagerMixin, TemplateView):
    template_name = 'filemanager/filemanager_upload.html'
    extra_breadcrumbs = [{
        'path': '#',
        'label': 'Upload'
    }]


class UploadFileView(FilemanagerMixin, View):
    def post(self, request, *args, **kwargs):
        if len(request.FILES) != 1:
            return HttpResponseBadRequest("Just a single file please.")

        # TODO: get filepath and validate characters in name, validate mime type and extension
        filename = self.fm.upload_file(filedata = request.FILES['files[]'])

        return HttpResponse(json.dumps({
            'files': [{'name': filename}],
        }))


class DirectoryCreateView(FilemanagerMixin, FormView):
    template_name = 'filemanager/filemanager_create_directory.html'
    form_class = DirectoryCreateForm
    extra_breadcrumbs = [{
        'path': '#',
        'label': 'Create directory'
    }]

    def get_success_url(self):
        return reverse_lazy('filemanager:browser') + '?path=' + self.fm.path

    def form_valid(self, form):
        self.fm.create_directory(form.cleaned_data.get('directory_name'))
        return super(DirectoryCreateView, self).form_valid(form)
