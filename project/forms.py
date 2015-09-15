from django import forms
from django.forms import ModelForm
from project.models import *


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'create_date','deadline','status')
