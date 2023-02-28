from django.urls import include, path
from rest_framework import routers

from ..viewsets import MetaViewSet

router = routers.DefaultRouter()
router.register(r'meta', MetaViewSet, basename='meta')

urlpatterns = [
    path('', include(router.urls)),
]
