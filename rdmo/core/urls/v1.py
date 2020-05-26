from django.urls import include, path

from rest_framework import routers

from ..viewsets import SettingsViewSet, SitesViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'settings', SettingsViewSet, basename='setting')
router.register(r'sites', SitesViewSet, basename='site')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('conditions/', include('rdmo.conditions.urls.v1')),
    path('domain/', include('rdmo.domain.urls.v1')),
    path('options/', include('rdmo.options.urls.v1')),
    path('projects/', include('rdmo.projects.urls.v1')),
    path('questions/', include('rdmo.questions.urls.v1')),
    path('tasks/', include('rdmo.tasks.urls.v1')),
    path('views/', include('rdmo.views.urls.v1')),

    path('core/', include(router.urls)),
]
