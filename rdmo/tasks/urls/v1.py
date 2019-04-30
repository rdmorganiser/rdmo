from django.urls import include, path

from rest_framework import routers

from ..viewsets import TaskViewSet

app_name = 'v1-tasks'

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='task')

urlpatterns = [
    path('', include(router.urls)),
]
