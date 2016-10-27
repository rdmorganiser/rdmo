from django.conf.urls import url, include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'conditions', ConditionViewSet, base_name='condition')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
router.register(r'relations', RelationViewSet, base_name='relation')

urlpatterns = [
    url(r'^', include(router.urls)),
]
