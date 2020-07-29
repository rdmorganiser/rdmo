from django.urls import re_path

from ..views import TasksExportView, TasksView

urlpatterns = [
    re_path(r'^$', TasksView.as_view(), name='tasks'),
    re_path(r'^export/(?P<format>[a-z]+)/$', TasksExportView.as_view(), name='tasks_export'),
]
