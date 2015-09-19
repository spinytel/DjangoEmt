from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.user_login),
    url(r'^logout', views.user_logout),
    url(r'^users/create', views.user_create),
    url(r'^users/(?P<user_id>[0-9]+)/edit', views.user_edit),
    url(r'^users/(?P<user_id>[0-9]+)/delete', views.user_delete),
    url(r'^users', views.user_all),
]
