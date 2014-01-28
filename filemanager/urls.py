from django.conf.urls import url, patterns

from filemanager.views import BrowserView, DetailView


urlpatterns = patterns('',
    url(r'^$', BrowserView.as_view(), name='browser'),
    url(r'^detail/$', DetailView.as_view(), name='detail'),
)
