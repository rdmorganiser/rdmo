from django.conf.urls import url, include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'entities', AttributeEntityViewSet, base_name='entity')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'options', OptionViewSet, base_name='option')
router.register(r'ranges', RangeViewSet, base_name='range')
router.register(r'verbosenames', VerboseNameViewSet, base_name='verbosename')
router.register(r'valuetypes', ValueTypeViewSet, base_name='valuestype')

urlpatterns = [
    url(r'^', include(router.urls)),
]
