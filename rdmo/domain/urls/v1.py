from django.urls import include, path

from rest_framework import routers

from ..viewsets import AttributeViewSet

app_name = 'v1-domain'

router = routers.DefaultRouter()
router.register(r'attributes', AttributeViewSet, basename='attribute')

urlpatterns = [
    path('', include(router.urls)),
]
