from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField('date created')
    deadline = models.DateTimeField('deadline')
    status = models.CharField(max_length=100)

class Milestone(models.Model):
    project_id = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    descriptions = models.TextField()
    start_date = models.DateTimeField('start date')
