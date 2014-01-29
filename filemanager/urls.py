from django.conf.urls import url, patterns
from django.views.decorators.csrf import csrf_exempt

from filemanager.views import BrowserView, DetailView, UploadView, UploadFileView


urlpatterns = patterns('',
    url(r'^$', BrowserView.as_view(), name='browser'),
    url(r'^detail/$', DetailView.as_view(), name='detail'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^upload/file/$', csrf_exempt(UploadFileView.as_view()), name='upload-file'),
)
