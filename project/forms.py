from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label='Project Name', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'Project Name'}))
    deadline = forms.DateTimeField(label='Deadline', widget=forms.TextInput(attrs={'class':'datetime_picker','placeholder':'Estimated Project Deadline','autocomplete':'off'}))
    project_file = forms.FileField(label='Project Files')
