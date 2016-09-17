from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', tasks, name='tasks'),
    url(r'^export/(?P<format>[a-z]+)/$', tasks_export, name='tasks_export'),
]
