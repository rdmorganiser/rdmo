from django.urls import include, re_path

from rest_framework import routers

from ..views import TasksView, TasksExportView, TasksImportXMLView

urlpatterns = [
    re_path(r'^$', TasksView.as_view(), name='tasks'),
    re_path(r'^export/(?P<format>[a-z]+)/$', TasksExportView.as_view(), name='tasks_export'),
    re_path(r'^import/(?P<format>[a-z]+)/$', TasksImportXMLView.as_view(), name='tasks_import'),
]
