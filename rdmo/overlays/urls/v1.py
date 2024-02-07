from django.urls import include, path

from rest_framework import routers

from ..viewsets import OverlayViewSet

app_name = 'v1-overlays'

router = routers.DefaultRouter()
router.register(r'overlays', OverlayViewSet, basename='overlay')

urlpatterns = [
    path('', include(router.urls)),
]
