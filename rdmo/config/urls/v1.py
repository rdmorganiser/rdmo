from django.urls import include, path

from rest_framework import routers

from ..viewsets import PluginViewSet

app_name = 'v1-config'

router = routers.DefaultRouter()
router.register(r'plugins', PluginViewSet, basename='plugin')

urlpatterns = [
    path('', include(router.urls)),
]
