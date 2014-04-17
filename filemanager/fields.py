from django import forms
from django.forms.widgets import Input


class FilemanagerWidget(Input):
    pass


class FilemanagerFormField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, path=None, *args, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.path = path
        super(FilemanagerFormField, self).__init__(*args, **kwargs)


class FilemanagerField(models.CharField):
    pass
