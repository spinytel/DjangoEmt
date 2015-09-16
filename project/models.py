from django.db import models
from authentication.models import Account


class Project(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField('date created')
    deadline = models.DateTimeField('deadline')
    status = models.CharField(max_length=100)


class MilestoneType(models.Model):
    types = models.CharField(max_length=100)


class Milestone(models.Model):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField('start date')
    due_date = models.DateTimeField('due date')
    user = models.ForeignKey(Account)
    type = models.ForeignKey(MilestoneType)
    budget = models.IntegerField()


class Ticket(models.Model):
    creator = models.ForeignKey(Account,related_name="creator_id")
    create_date = models.DateTimeField('date created')
    project = models.ForeignKey(Project)
    milestone = models.ForeignKey(Milestone)
    assign_person = models.ForeignKey(Account,related_name="assign_person_id")
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=100)
    priority = models.IntegerField()
    estimate = models.CharField(max_length=100)


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket)
    create_date = models.DateTimeField('date created')
    creator = models.ForeignKey(Account)
    prev_status = models.CharField(max_length=100)
    curr_status = models.CharField(max_length=100)
    details = models.TextField()


class TicketFile(models.Model):
    ticket = models.ForeignKey(Ticket)
    file_name = models.CharField(max_length=100)


class ProjectFile(models.Model):
    project = models.ForeignKey(Project)
    file_name = models.CharField(max_length=100)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.file_name

class ProjectMember(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(Account)
    member_type = models.IntegerField()
