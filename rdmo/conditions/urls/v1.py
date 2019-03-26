from django.urls import include, path

from rest_framework import routers

from ..viewsets import ConditionApiViewSet

app_name = 'api-v1-conditions'

router = routers.DefaultRouter()
router.register(r'conditions', ConditionApiViewSet, base_name='condition')

urlpatterns = [
    path('', include(router.urls)),
]
