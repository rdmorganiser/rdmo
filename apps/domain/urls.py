from django.conf.urls import url, include

from rest_framework import routers

from .views import DomainView, DomainExportView
from .viewsets import (
    AttributeEntityViewSet,
    AttributeViewSet,
    RangeViewSet,
    VerboseNameViewSet,
    ValueTypeViewSet,
    OptionSetViewSet,
    ConditionViewSet,
    AttributeEntityApiViewSet,
    AttributeApiViewSet
)

# regular views

domain_patterns = [
    url(r'^$', DomainView.as_view(), name='domain'),
    url(r'^export/(?P<format>[a-z]+)/$', DomainExportView.as_view(), name='domain_export'),
]

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'entities', AttributeEntityViewSet, base_name='entity')
internal_router.register(r'attributes', AttributeViewSet, base_name='attribute')
internal_router.register(r'ranges', RangeViewSet, base_name='range')
internal_router.register(r'verbosenames', VerboseNameViewSet, base_name='verbosename')
internal_router.register(r'valuetypes', ValueTypeViewSet, base_name='valuestype')
internal_router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
internal_router.register(r'conditions', ConditionViewSet, base_name='condition')

domain_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'entities', AttributeEntityApiViewSet, base_name='entity')
api_router.register(r'attributes', AttributeApiViewSet, base_name='attribute')

domain_patterns_api = [
    url(r'^', include(api_router.urls)),
]
