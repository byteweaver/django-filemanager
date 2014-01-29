from django.conf.urls import url, patterns

from filemanager.views import BrowserView, DetailView, UploadView


urlpatterns = patterns('',
    url(r'^$', BrowserView.as_view(), name='browser'),
    url(r'^detail/$', DetailView.as_view(), name='detail'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
)
