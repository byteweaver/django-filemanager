from django import forms
from django.forms.widgets import Input


class FilemanagerWidget(Input):
    input_type = 'text'

    def __init__(self, attrs={}):
        super(FilemanagerWidget, self).__init__(attrs)
        self.path = attrs.get('path', '')
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
        super(FilemanagerWidget, self).__init__(attrs)


class FilemanagerFormField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, path=None, *args, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.path = path
        super(FilemanagerFormField, self).__init__(*args, **kwargs)


class FilemanagerField(models.CharField):
    description = "FilemanagerField"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path', '')
        return super(FilemanagerField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        attrs = {
            'path': self.path,
        }
        defaults = {
            'form_class': FilemanagerFormField,
            'widget': FilemanagerWidget(attrs=attrs),
            'path': self.path,
        }
        return super(FilemanagerField, self).formfield(**defaults)
