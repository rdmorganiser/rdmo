from django.conf.urls import url, include

from rest_framework import routers

from .views import (
    OptionSetViewSet,
    OptionViewSet,
    ConditionViewSet
)

router = routers.DefaultRouter()
router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
router.register(r'options', OptionViewSet, base_name='option')
router.register(r'conditions', ConditionViewSet, base_name='condition')

urlpatterns = [
    url(r'^', include(router.urls)),
]
