from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.user_login, name='user_login'),
    url(r'^logout', views.user_logout, name='user_logout'),
    url(r'^users/create', views.user_create, name='user_create'),
    url(r'^users/(?P<user_id>[0-9]+)/edit', views.user_edit, name='user_edit'),
    url(r'^users/(?P<user_id>[0-9]+)/delete', views.user_delete, name='user_delete'),
    url(r'^users', views.user_all, name='user_all'),
]
