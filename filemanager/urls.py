from django.conf.urls import url, patterns

from filemanager.views import BrowserView


urlpatterns = patterns('',
    url(r'^$', BrowserView.as_view(), name='browser'),
)
