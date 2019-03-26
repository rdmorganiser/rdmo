from django.urls import include, path

from rest_framework import routers

from ..viewsets import ProjectApiViewSet, SnapshotApiViewSet, ValueApiViewSet

app_name = 'api-v1-projects'

router = routers.DefaultRouter()
router.register(r'projects', ProjectApiViewSet, base_name='project')
router.register(r'snapshots', SnapshotApiViewSet, base_name='snapshot')
router.register(r'values', ValueApiViewSet, base_name='value')

urlpatterns = [
    path('', include(router.urls)),
]
