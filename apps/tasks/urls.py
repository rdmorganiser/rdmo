from django.conf.urls import url

from .views import TasksView, TasksExportView

urlpatterns = [
    url(r'^$', TasksView.as_view(), name='tasks'),
    url(r'^export/(?P<format>[a-z]+)/$', TasksExportView.as_view(), name='tasks_export'),
]
