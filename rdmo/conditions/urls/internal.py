from django.urls import include, path

from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from ..viewsets import (AttributeViewSet, ConditionViewSet,
                        OptionViewSet, RelationViewSet)

app_name = 'internal-conditions'

router = routers.DefaultRouter()
router.register(r'conditions', ConditionViewSet, base_name='condition')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'options', OptionViewSet, base_name='option')
router.register(r'relations', RelationViewSet, base_name='relation')
router.register(r'settings', SettingsViewSet, base_name='setting')

urlpatterns = [
    path('', include(router.urls)),
]
