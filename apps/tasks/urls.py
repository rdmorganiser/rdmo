from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', tasks, name='tasks'),
    url(r'^export/xml/$', tasks_export_xml, name='tasks_export_xml'),
    url(r'^export/(?P<format>[a-z]+)/$', tasks_export, name='tasks_export'),
]
