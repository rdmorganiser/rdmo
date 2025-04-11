from django.urls import include, path

from rest_framework import routers

from rdmo.core.viewsets import GroupViewSet, SettingsViewSet, SitesViewSet, TemplatesViewSet

app_name = 'v1-core'

router = routers.DefaultRouter()
router.register(r'settings', SettingsViewSet, basename='setting')
router.register(r'sites', SitesViewSet, basename='site')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'templates', TemplatesViewSet, basename='template')

urlpatterns = [
    path('', include(router.urls)),
]
