from django import forms
from django.forms.widgets import Input


class FilemanagerWidget(Input):
    pass


class FilemanagerFormField(forms.CharField):
    pass
