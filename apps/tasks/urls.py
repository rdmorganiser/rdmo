from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import TasksView, TasksExportView

urlpatterns = [
    url(r'^$', cache_page(settings.CACHE_TIMEOUT)(TasksView.as_view()), name='tasks'),
    url(r'^export/(?P<format>[a-z]+)/$', TasksExportView.as_view(), name='tasks_export'),
]
