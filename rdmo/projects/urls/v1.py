from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from ..viewsets import (CatalogViewSet, MembershipViewSet,
                        ProjectMembershipViewSet, ProjectQuestionSetViewSet,
                        ProjectSnapshotViewSet, ProjectValueViewSet,
                        ProjectViewSet, QuestionSetViewSet, SnapshotViewSet,
                        ValueViewSet)

app_name = 'v1-projects'

router = ExtendedDefaultRouter()
project_route = router.register(r'projects', ProjectViewSet, basename='project')
project_route.register(r'memberships', ProjectMembershipViewSet, basename='project-membership',
                       parents_query_lookups=['project'])
project_route.register(r'snapshots', ProjectSnapshotViewSet, basename='project-snapshot',
                       parents_query_lookups=['project'])
project_route.register(r'values', ProjectValueViewSet, basename='project-value',
                       parents_query_lookups=['project'])
project_route.register(r'questionsets', ProjectQuestionSetViewSet, basename='project-questionset',
                       parents_query_lookups=['project'])
router.register(r'memberships', MembershipViewSet, basename='membership')
router.register(r'snapshots', SnapshotViewSet, basename='snapshot')
router.register(r'values', ValueViewSet, basename='value')
router.register(r'questionsets', QuestionSetViewSet, basename='questionset')
router.register(r'catalogs', CatalogViewSet, basename='catalog')


urlpatterns = [
    path('', include(router.urls)),
]
