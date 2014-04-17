# django-filemanager

Template for reusable django applications.

All following sections are just dummies and may not work as excepted.

## Key features

* Reusable template for new reusable django applications
* ...

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
        url(r'^your-url/$', include('filemanager.urls', namespace='{{ app_name }}')),
        ...
    )

## Setup

Define paths for `MEDIA_ROOT` and `MEDIA_URL` in your django settings file or override the filemanager settings for `FILEMANAGER_MEDIA_ROOT` and `FILEMANAGER_MEDIA_URL`.

Make sure the base folder defined in your settings for filemanager does exist. By default it is located at `MEDIA_ROOT/uploads`.
