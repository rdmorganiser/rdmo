from django.urls import include, path

from rest_framework_extensions.routers import ExtendedDefaultRouter

from ..viewsets import (
    ProjectViewSet,
    ProjectSnapshotViewSet,
    ProjectValueViewSet,
    SnapshotViewSet,
    ValueViewSet,
    QuestionSetViewSet,
    CatalogViewSet
)

app_name = 'v1-projects'

router = ExtendedDefaultRouter()
project_route = router.register(r'projects', ProjectViewSet, base_name='project')
project_route.register(r'snapshots', ProjectSnapshotViewSet, base_name='project-snapshot',
                       parents_query_lookups=['project'])
project_route.register(r'values', ProjectValueViewSet, base_name='project-value',
                       parents_query_lookups=['project'])
router.register(r'snapshots', SnapshotViewSet, base_name='snapshot')
router.register(r'values', ValueViewSet, base_name='value')
router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
router.register(r'catalogs', CatalogViewSet, base_name='catalog')

urlpatterns = [
    path('', include(router.urls)),
]
