from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.project_create),
    url(r'^(?P<project_id>[0-9]+)/edit/', views.project_edit),
    url(r'^(?P<project_id>[0-9]+)/milestone/create/', views.milestone_create),
]
