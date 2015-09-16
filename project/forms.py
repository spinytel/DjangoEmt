from django import forms
from django.utils import timezone

class ProjectForm(forms.Form):
    name = forms.CharField(label='Project Name', max_length=200, required=True)
    deadline = forms.DateTimeField(label='Deadline', widget=forms.TextInput(attrs={'class':'datetime_picker'}))
