from django.urls import include, path

from rest_framework_extensions.routers import ExtendedDefaultRouter

from ..viewsets import (
    IntegrationViewSet,
    InviteViewSet,
    IssueViewSet,
    MembershipViewSet,
    ProjectIntegrationViewSet,
    ProjectInviteViewSet,
    ProjectIssueViewSet,
    ProjectMembershipViewSet,
    ProjectPageViewSet,
    ProjectSnapshotViewSet,
    ProjectValueViewSet,
    ProjectViewSet,
    SnapshotViewSet,
    ValueViewSet,
)

app_name = 'v1-projects'

router = ExtendedDefaultRouter()
project_route = router.register(r'projects', ProjectViewSet, basename='project')
project_route.register(r'memberships', ProjectMembershipViewSet, basename='project-membership',
                       parents_query_lookups=['project'])
project_route.register(r'integrations', ProjectIntegrationViewSet, basename='project-integration',
                       parents_query_lookups=['project'])
project_route.register(r'invites', ProjectInviteViewSet, basename='project-invite',
                       parents_query_lookups=['project'])
project_route.register(r'issues', ProjectIssueViewSet, basename='project-issue',
                       parents_query_lookups=['project'])
project_route.register(r'snapshots', ProjectSnapshotViewSet, basename='project-snapshot',
                       parents_query_lookups=['project'])
project_route.register(r'values', ProjectValueViewSet, basename='project-value',
                       parents_query_lookups=['project'])
project_route.register(r'pages', ProjectPageViewSet, basename='project-page',
                       parents_query_lookups=['project'])
router.register(r'memberships', MembershipViewSet, basename='membership')
router.register(r'integrations', IntegrationViewSet, basename='integration')
router.register(r'invites', InviteViewSet, basename='invite')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'snapshots', SnapshotViewSet, basename='snapshot')
router.register(r'values', ValueViewSet, basename='value')


urlpatterns = [
    path('', include(router.urls)),
]
