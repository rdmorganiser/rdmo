from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from ..viewsets import (ProjectQuestionSetViewSet, ProjectSnapshotViewSet,
                        ProjectValueViewSet, ProjectViewSet, SnapshotViewSet,
                        ValueViewSet)


app_name = 'v1-projects'

router = ExtendedDefaultRouter()
project_route = router.register(r'projects', ProjectViewSet, basename='project')
project_route.register(r'snapshots', ProjectSnapshotViewSet, basename='project-snapshot',
                       parents_query_lookups=['project'])
project_route.register(r'values', ProjectValueViewSet, basename='project-value',
                       parents_query_lookups=['project'])
project_route.register(r'questionsets', ProjectQuestionSetViewSet, basename='project-questionset',
                       parents_query_lookups=['project'])
router.register(r'snapshots', SnapshotViewSet, basename='snapshot')
router.register(r'values', ValueViewSet, basename='value')

urlpatterns = [
    path('', include(router.urls)),
]
