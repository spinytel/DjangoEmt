from django.db import models
from authentication.models import Account


class Project(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField('date created')
    deadline = models.DateTimeField('deadline')
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.id


class MilestoneType(models.Model):
    types = models.CharField(max_length=100)

    def __str__(self):
        return self.id


class Milestone(models.Model):
    project_id = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField('start date')
    due_date = models.DateTimeField('due date')
    user_id = models.ForeignKey(Account)
    type_id = models.ForeignKey(MilestoneType)
    budget = models.IntegerField()

    def __str__(self):
        return self.id


class Ticket(models.Model):
    creator_id = models.ForeignKey(Account,related_name="creator_id")
    create_date = models.DateTimeField('date created')
    project_id = models.ForeignKey(Project)
    mileston_id = models.ForeignKey(Milestone)
    assign_person_id = models.ForeignKey(Account,related_name="assign_person_id")
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=100)
    priority = models.IntegerField()
    estimate = models.CharField(max_length=100)

    def __str__(self):
        return self.id


class Comment(models.Model):
    ticket_id = models.ForeignKey(Ticket)
    create_date = models.DateTimeField('date created')
    creator_id = models.ForeignKey(Account)
    prev_status = models.CharField(max_length=100)
    curr_status = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.id


class TicketFile(models.Model):
    ticket_id = models.ForeignKey(Ticket)
    file_name = models.CharField(max_length=100)

    def __str__(self):
        return self.id


class ProjectFile(models.Model):
    ticket_id = models.ForeignKey(Project)
    file_name = models.CharField(max_length=100)

    def __str__(self):
        return self.id


class ProjectMember(models.Model):
    project_id = models.ForeignKey(Project)
    user_id = models.ForeignKey(Account)
    member_type = models.IntegerField()

    def __str__(self):
        return self.id
