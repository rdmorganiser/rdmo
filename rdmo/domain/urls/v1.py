from django.urls import include, path

from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from ..viewsets import AttributeViewSet


app_name = 'v1-domain'

router = routers.DefaultRouter()
router.register(r'attributes', AttributeViewSet, base_name='attribute')

urlpatterns = [
    path('', include(router.urls)),
]
