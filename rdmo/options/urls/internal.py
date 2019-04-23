from django.urls import include, path

from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from ..viewsets import ConditionViewSet, OptionSetViewSet, OptionViewSet

app_name = 'internal-options'

router = routers.DefaultRouter()
router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
router.register(r'options', OptionViewSet, base_name='option')
router.register(r'conditions', ConditionViewSet, base_name='condition')
router.register(r'settings', SettingsViewSet, base_name='setting')

urlpatterns = [
    path('', include(router.urls)),
]
