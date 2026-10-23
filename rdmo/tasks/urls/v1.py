from django.urls import include, path

from rest_framework import routers

from ..viewsets import TaskAreaViewSet, TaskTypeViewSet, TaskViewSet

app_name = 'v1-tasks'

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tasktypes', TaskTypeViewSet, basename='tasktype')
router.register(r'taskareas', TaskAreaViewSet, basename='taskarea')

urlpatterns = [
    path('', include(router.urls)),
]
