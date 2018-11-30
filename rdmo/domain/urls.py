from django.conf.urls import url, include

from rest_framework import routers

from .views import DomainView, DomainExportView, DomainImportXMLView
from .viewsets import (
    AttributeViewSet,
    AttributeApiViewSet
)

# regular views

domain_patterns = [
    url(r'^$', DomainView.as_view(), name='domain'),
    url(r'^export/(?P<format>[a-z]+)/$', DomainExportView.as_view(), name='domain_export'),
    url(r'^import/(?P<format>[a-z]+)/$', DomainImportXMLView.as_view(), name='domain_import'),
]

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'attributes', AttributeViewSet, base_name='attribute')

domain_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'attributes', AttributeApiViewSet, base_name='attribute')

domain_patterns_api = [
    url(r'^', include(api_router.urls)),
]
