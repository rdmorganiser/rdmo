from django.urls import include, path

from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from ..viewsets import ViewViewSet

app_name = 'internal-views'

router = routers.DefaultRouter()
router.register(r'views', ViewViewSet, base_name='view')
router.register(r'settings', SettingsViewSet, base_name='setting')

urlpatterns = [
    path('', include(router.urls)),
]
