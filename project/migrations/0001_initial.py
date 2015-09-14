# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(verbose_name=b'date created')),
                ('prev_status', models.CharField(max_length=100)),
                ('curr_status', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('creator_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField(verbose_name=b'start date')),
                ('due_date', models.DateTimeField(verbose_name=b'due date')),
                ('budget', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MilestoneType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('types', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(verbose_name=b'date created')),
                ('deadline', models.DateTimeField(verbose_name=b'deadline')),
                ('status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=100)),
                ('ticket_id', models.ForeignKey(to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_type', models.IntegerField()),
                ('project_id', models.ForeignKey(to='project.Project')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(verbose_name=b'date created')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=100)),
                ('priority', models.IntegerField()),
                ('estimate', models.CharField(max_length=100)),
                ('assign_person_id', models.ForeignKey(related_name='assign_person_id', to=settings.AUTH_USER_MODEL)),
                ('creator_id', models.ForeignKey(related_name='creator_id', to=settings.AUTH_USER_MODEL)),
                ('mileston_id', models.ForeignKey(to='project.Milestone')),
                ('project_id', models.ForeignKey(to='project.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TicketFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=100)),
                ('ticket_id', models.ForeignKey(to='project.Ticket')),
            ],
        ),
        migrations.AddField(
            model_name='milestone',
            name='project_id',
            field=models.ForeignKey(to='project.Project'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='type_id',
            field=models.ForeignKey(to='project.MilestoneType'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='ticket_id',
            field=models.ForeignKey(to='project.Ticket'),
        ),
    ]
