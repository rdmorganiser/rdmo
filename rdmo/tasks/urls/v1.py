from django.urls import include, path

from rest_framework import routers

from ..viewsets import TaskToggleCurrentSiteViewSet, TaskViewSet

app_name = 'v1-tasks'

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-toggle-site', TaskToggleCurrentSiteViewSet, basename='task-toggle-site')

urlpatterns = [
    path('', include(router.urls)),
]
