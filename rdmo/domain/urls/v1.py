from django.urls import include, path

from rest_framework import routers

from ..viewsets import AttributeApiViewSet

app_name = 'api-v1-domain'

router = routers.DefaultRouter()
router.register(r'attributes', AttributeApiViewSet, base_name='attribute')

urlpatterns = [
    path('', include(router.urls)),
]
