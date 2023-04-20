from django.urls import include, path
from rest_framework import routers

from ..viewsets import ImportViewSet, MetaViewSet

app_name = 'v1-management'

router = routers.DefaultRouter()
router.register(r'meta', MetaViewSet, basename='meta')
router.register(r'import', ImportViewSet, basename='import')

urlpatterns = [
    path('', include(router.urls)),
]
