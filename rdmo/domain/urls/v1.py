from django.urls import include, path

from rdmo.core.views import SettingsViewSet
from rest_framework import routers

from ..viewsets import AttributeViewSet

app_name = 'v1-domain'

router = routers.DefaultRouter()
try:
    router.register(r'attributes', AttributeViewSet, basename='attribute')
except TypeError:
    router.register(r'attributes', AttributeViewSet, base_name='attribute')

urlpatterns = [
    path('', include(router.urls)),
]
