from django.conf.urls import url, include

from rest_framework import routers

from .views import TasksView, TasksExportView
from .viewsets import TaskViewSet, TimeFrameViewSet, AttributeViewSet, ConditionViewSet, TaskApiViewSet

# regular views

tasks_patterns = [
    url(r'^$', TasksView.as_view(), name='tasks'),
    url(r'^export/(?P<format>[a-z]+)/$', TasksExportView.as_view(), name='tasks_export'),
]

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'tasks', TaskViewSet, base_name='task')
internal_router.register(r'timeframes', TimeFrameViewSet, base_name='timeframe')
internal_router.register(r'attributes', AttributeViewSet, base_name='attribute')
internal_router.register(r'conditions', ConditionViewSet, base_name='condition')

tasks_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'tasks', TaskApiViewSet, base_name='task')

tasks_patterns_api = [
    url(r'^', include(api_router.urls)),
]
