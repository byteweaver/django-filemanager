# django-filemanager

A simple and standalone file manager and browser for django projects. Supports multiple instances which can be used within the admin area or for the frontend as well.

## Key features

* Standalone file browser and manager
* No external dependencies except django
* Feature rich uploader included (jQuery File Upload)
* Based on django storage backend

## Installation

If you want to install the latest stable release from PyPi:

    $ pip install django-filemanager

If you want to install the latest development version from GitHub:

    $ pip install -e git://github.com/byteweaver/django-filemanager#egg=django-filemanager

Add `filemanager` to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'filemanager',
        ...
    )

Hook this app into your ``urls.py``:

    urlpatterns = patterns('',
        ...
        url(r'^your-url/$', include('filemanager.urls', namespace='filemanager')),
        ...
    )

## Setup

### Base template

If you like to use the basic templates included you have to make sure your project does meet the following requirements. The filemanger does require a base template called `base.html` to extend from or you to override the `filemanager/filemanager_base.html` template. Within your template you have to define a block named `content`, like in the following example:

    <html>
      <head>...</head>
      <body>
        {% block content %}{% endblock %}
      </body>
    </html>

### Directory settings

Define paths for `MEDIA_ROOT` and `MEDIA_URL` in your django settings file or override the filemanager settings for `FILEMANAGER_MEDIA_ROOT` and `FILEMANAGER_MEDIA_URL`.

Make sure the base folder defined in your settings for filemanager does exist. By default it is located at `MEDIA_ROOT/uploads`.
