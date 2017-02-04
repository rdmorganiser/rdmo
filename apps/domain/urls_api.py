from django.conf.urls import include, url
from rest_framework import routers

from .views import (
    AttributeEntityViewSet,
    AttributeViewSet,
    RangeViewSet,
    VerboseNameViewSet,
    ValueTypeViewSet,
    OptionSetViewSet,
    ConditionViewSet,
)

router = routers.DefaultRouter()
router.register(r'entities', AttributeEntityViewSet, base_name='entity')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'ranges', RangeViewSet, base_name='range')
router.register(r'verbosenames', VerboseNameViewSet, base_name='verbosename')
router.register(r'valuetypes', ValueTypeViewSet, base_name='valuestype')
router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
router.register(r'conditions', ConditionViewSet, base_name='condition')

urlpatterns = [
    url(r'^', include(router.urls)),
]
