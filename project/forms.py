from django import forms
from django.utils import timezone
from .models import Project, ProjectMember, MilestoneType, Milestone
from authentication.models import Account

# project create form @rejoan
class ProjectForm(forms.Form):
    name = forms.CharField(label='Project Name', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'Project Name'}))
    deadline = forms.DateTimeField(label='Deadline', widget=forms.DateTimeInput(attrs={'class':'datetime_picker','placeholder':'Estimated Project Deadline','autocomplete':'off'}))
    project_file = forms.FileField(label='Project Files')

# project edit form @rejoan
class ProjectEditForm(forms.Form):
    name = forms.CharField(label='Project Name', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder':'Project Name'}))
    deadline = forms.DateTimeField(label='Deadline',widget=forms.DateTimeInput(attrs={'class':'datetime_picker','placeholder':'Estimated Project Deadline','autocomplete':'off'}))
    project_file = forms.FileField(label='Project Files',required=False)
    project_update_id = forms.CharField()

# project create form @rejoan
class TicketForm(forms.Form):
    STATUS_CHOICES = (
         ('In Progress', (
           ('New', 'New'),
           ('Accepted', 'Accepted'),
           ('Test', 'Test'),
          )
         ),
         ('Closed', (
           ('Fixed', 'Fixed'),
           ('Invalid', 'Invalid'),
          )
         ),
        )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Status', widget=forms.Select(attrs = {'class':'p_selection selection'}))

    PRIORITY_CHOICES = (
           ('1', 'Highest (1)'),
           ('2', 'High(2)'),
           ('3', 'Normal(3)'),
           ('4', 'Low(4)'),
           ('5', 'Lowest(3)'),
         )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=True, label='Status', widget=forms.Select(attrs = {'class':'p_selection selection'}))

    ESTIMATE_CHOICES = (
           ('None', 'None'),
           ('Small', 'Small'),
           ('Medium', 'Medium'),
           ('Large', 'Large'),
         )
    estimate = forms.ChoiceField(choices=ESTIMATE_CHOICES, required=True, label='Estimate', widget=forms.Select(attrs = {'class':'p_selection selection'}))

    title = forms.CharField(max_length=200, required = True, widget = forms.TextInput(attrs = {'placeholder':'Summary of new ticket'}))
    description = forms.CharField(widget = forms.Textarea)
    ticket_file = forms.FileField(label = 'Ticket Files',required = False)
    #assign = [(a.user.get_id(), a.user.get_full_name()) for a in ProjectMember.objects.filter(project__id = project_id)]
    project_id = forms.CharField()


# project edit form @rejoan
class TicketEditForm(forms.Form):
    STATUS_CHOICES = (
         ('In Progress', (
           ('New', 'New'),
           ('Accepted', 'Accepted'),
           ('Test', 'Test'),
          )
         ),
         ('Closed', (
           ('Fixed', 'Fixed'),
           ('Invalid', 'Invalid'),
          )
         ),
        )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Status', widget=forms.Select(attrs = {'class':'p_selection selection'}))

    PRIORITY_CHOICES = (
           ('1', 'Highest (1)'),
           ('2', 'High(2)'),
           ('3', 'Normal(3)'),
           ('4', 'Low(4)'),
           ('5', 'Lowest(3)'),
         )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=True, label='Status', widget=forms.Select(attrs = {'class':'p_selection selection'}))

    ESTIMATE_CHOICES = (
           ('None', 'None'),
           ('Small', 'Small'),
           ('Medium', 'Medium'),
           ('Large', 'Large'),
         )
    estimate = forms.ChoiceField(choices=ESTIMATE_CHOICES, required=True, label='Estimate', widget=forms.Select(attrs = {'class':'p_selection selection'}))

    title = forms.CharField(max_length=200, required = True, widget = forms.TextInput(attrs = {'placeholder':'Summary of new ticket'}))
    description = forms.CharField(widget = forms.Textarea)
    ticket_file = forms.FileField(label = 'Ticket Files', required=False)
    #assign = [(a.user.get_id(), a.user.get_full_name()) for a in ProjectMember.objects.filter(project__id = project_id)]
    project_id = forms.CharField()
    ticket_id = forms.CharField()


# Author : @mamun0024
class MilestoneForm(forms.Form):
    def __init__(self,*args,**kwargs):
        passing_product_id = kwargs.pop("passing_id")     # passing_product_id is the parameter passed from views.py
        super(MilestoneForm, self).__init__(*args,**kwargs)
        self.fields['project_id'] = forms.IntegerField(widget=forms.TextInput(attrs={'type':'hidden','value':passing_product_id}))
        self.fields['title'] = forms.CharField(max_length=200,required=True, widget=forms.TextInput(attrs={'placeholder':'Enter a title for milestone'}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write an optional description'}),max_length=10000, required=True)
        self.fields['start_date'] = forms.DateTimeField(label='Start Date', widget=forms.TextInput(attrs={'class':'dp_milestone_start_date', 'placeholder':'Start Date'}), required=True)
        self.fields['due_date'] = forms.DateTimeField(label='Due Date', widget=forms.TextInput(attrs={'class':'dp_milestone_due_date', 'placeholder':'Due Date'}), required=True)
        self.fields['budget'] = forms.IntegerField(label='Budget', max_value=99999999, required=True, widget=forms.TextInput(attrs={'placeholder':'Budget'}))

        self.fields['m_type'] = forms.ChoiceField(label="Milestone type", choices=[(c.id, c.types) for c in MilestoneType.objects.order_by('id')], widget=forms.Select(attrs={'class':'p_selection selection'}))
        self.fields['m_responsible'] = forms.ChoiceField(label="Responsible", choices=[(c.user.get_id(), c.user.get_full_name()) for c in ProjectMember.objects.filter(project__id = passing_product_id)], widget=forms.Select(attrs={'class':'p_selection selection'}))


# Author : @mamun0024
class MilestoneEditForm(forms.Form):
    class Meta:
        model = Milestone

    def __init__(self,*args,**kwargs):
        passing_milestone_id = kwargs.pop("passing_milestone_id")     # passing_milestone_id is the parameter passed from views.py
        super(MilestoneEditForm, self).__init__(*args,**kwargs)
        milestone_details = Milestone.objects.get(pk=int(passing_milestone_id))
        self.fields['project_id'] = forms.IntegerField(widget=forms.TextInput(attrs={'type':'hidden','value':milestone_details.project_id}))
        self.fields['title'] = forms.CharField(max_length=200,required=True, widget=forms.TextInput(attrs={'placeholder':'Enter a title for milestone','value':milestone_details.title}))
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write an optional description'}),max_length=10000, required=True, initial=milestone_details.description)
        self.fields['start_date'] = forms.DateTimeField(label='Start Date', widget=forms.TextInput(attrs={'class':'dp_milestone_start_date', 'placeholder':'Start Date','value':milestone_details.start_date.strftime("%Y-%m-%d")}), required=True)
        self.fields['due_date'] = forms.DateTimeField(label='Due Date', widget=forms.TextInput(attrs={'class':'dp_milestone_due_date', 'placeholder':'Due Date','value':milestone_details.due_date.strftime("%Y-%m-%d")}), required=True)
        self.fields['budget'] = forms.IntegerField(label='Budget', max_value=99999999, required=True, widget=forms.TextInput(attrs={'placeholder':'Budget','value':milestone_details.budget}))

        self.fields['m_type'] = forms.ChoiceField(label="Milestone type", choices=[(c.id, c.types) for c in MilestoneType.objects.order_by('id')], widget=forms.Select(attrs={'class':'p_selection selection'}), initial=milestone_details.type_id)
        self.fields['m_responsible'] = forms.ChoiceField(label="Responsible", choices=[(c.user.get_id(), c.user.get_full_name()) for c in ProjectMember.objects.filter(project__id = milestone_details.project_id)], widget=forms.Select(attrs={'class':'p_selection selection'}), initial=milestone_details.user_id)
