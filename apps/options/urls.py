from django.conf.urls import url, include

from rest_framework import routers

from .views import OptionsView, OptionsExportView
from .viewsets import (
    OptionSetViewSet,
    OptionViewSet,
    ConditionViewSet,
    OptionSetApiViewSet,
    OptionApiViewSet
)

# regular views

options_patterns = [
    url(r'^$', OptionsView.as_view(), name='options'),
    url(r'^export/(?P<format>[a-z]+)/$', OptionsExportView.as_view(), name='options_export'),
]

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
internal_router.register(r'options', OptionViewSet, base_name='option')
internal_router.register(r'conditions', ConditionViewSet, base_name='condition')

options_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'optionsets', OptionSetApiViewSet, base_name='optionset')
api_router.register(r'options', OptionApiViewSet, base_name='option')

options_patterns_api = [
    url(r'^', include(api_router.urls)),
]
