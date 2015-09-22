from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^create/$', views.project_create,name="project_create"),
    url(r'^(?P<project_id>[0-9]+)/edit/', views.project_edit, name="project_edit"),
    url(r'^(?P<project_id>[0-9]+)/ticket/create/', views.ticket_create, name="ticket_create"),
    url(r'^(?P<project_id>[0-9]+)/ticket/(?P<ticket_id>[0-9]+)/edit/', views.ticket_edit, name="ticket_edit"),
    url(r'^(?P<project_id>[0-9]+)/tickets/', views.tickets, name="tickets"),
    url(r'^(?P<project_id>[0-9]+)/milestone/create', views.milestone_create, name='milestone_create'),
    url(r'^(?P<project_id>[0-9]+)/milestone/(?P<milestone_id>[0-9]+)/edit', views.milestone_edit, name='milestone_edit'),
    url(r'^(?P<project_id>[0-9]+)/milestone/(?P<milestone_id>[0-9]+)/delete', views.milestone_delete, name='milestone_delete'),
    url(r'^(?P<project_id>[0-9]+)/milestone', views.milestone_all, name='milestone_all'),
    url(r'^$', views.projects, name="projects"),

]
