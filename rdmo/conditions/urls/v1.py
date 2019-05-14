from django.urls import include, path

from rest_framework import routers

from ..viewsets import ConditionViewSet, RelationViewSet

app_name = 'v1-conditions'

router = routers.DefaultRouter()
router.register(r'conditions', ConditionViewSet, basename='condition')
router.register(r'relations', RelationViewSet, basename='relation')

urlpatterns = [
    path('', include(router.urls)),
]
