from django.urls import include, path

from rest_framework import routers

from ..viewsets import TaskApiViewSet

app_name = 'api-v1-tasks'

router = routers.DefaultRouter()
router.register(r'tasks', TaskApiViewSet, base_name='task')

urlpatterns = [
    path('', include(router.urls)),
]
