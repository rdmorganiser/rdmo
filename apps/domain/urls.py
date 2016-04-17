from django.conf.urls import url, include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'entities', AttributeEntityViewSet, base_name='entity')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'attributesets', AttributeSetViewSet, base_name='attributeset')
router.register(r'valuetypes', ValueTypeViewSet, base_name='valuestype')

urlpatterns = [
    url(r'^$', domain, name='domain'),
    url(r'^api/', include(router.urls)),
]
