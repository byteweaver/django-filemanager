from django import forms
from django.db import models
from django.core.urlresolvers import reverse
from django.forms.widgets import Input
from django.template.loader import render_to_string


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

    def render(self, name, value, attrs=None):
        url = reverse("filemanager:browser")
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['url'] = url
        final_attrs['path'] = self.path
        return render_to_string('filemanager/filemanager_field.html', locals())

    class Media:
        css = {
            'all': ('css/filemanager.css',),
        }
        js = ('js/filemanager.js',)


class FilemanagerFormField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, path=None, *args, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.path = path
        super(FilemanagerFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(FilemanagerFormField, self).clean(value)
        if value == '':
            return value
        return value


class FilemanagerField(models.CharField):
    description = "FilemanagerField"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path', '')
        return super(FilemanagerField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        print("to_python", value)
        if not value:
            return value
        return value

    def get_prep_value(self, value):
        print("get_prep_value", value)
        if not value:
            return value
        return value

    def value_to_string(self, obj):
        print("value_to_string", obj)
        value = self._get_val_from_obj(obj)
        if not value:
            return value
        return value

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
