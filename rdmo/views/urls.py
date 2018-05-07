from django.conf.urls import url, include

from rest_framework import routers

from .views import ViewsView, ViewsExportView, ViewsImportXMLView
from .viewsets import ViewViewSet, ViewApiViewSet

# regular views

views_patterns = [
    url(r'^$', ViewsView.as_view(), name='views'),
    url(r'^export/(?P<format>[a-z]+)/$', ViewsExportView.as_view(), name='views_export'),
    url(r'^import/(?P<format>[a-z]+)/$', ViewsImportXMLView.as_view(), name='views_import'),
]

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'views', ViewViewSet, base_name='view')

views_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'views', ViewApiViewSet, base_name='view')

views_patterns_api = [
    url(r'^', include(api_router.urls)),
]
