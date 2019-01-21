from django.conf.urls import include, url
from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from .views import CatalogExportView, CatalogImportXMLView, CatalogsView
from .viewsets import (AttributeViewSet, CatalogApiViewSet, CatalogViewSet,
                       ConditionViewSet, OptionSetViewSet, QuestionApiViewSet,
                       QuestionSetApiViewSet, QuestionSetViewSet,
                       QuestionViewSet, SectionApiViewSet, SectionViewSet,
                       ValueTypeViewSet, WidgetTypeViewSet)

# regular views

questions_patterns = [
    url(r'^catalogs/(?P<pk>[0-9]+)/export/(?P<format>[a-z]+)/$', CatalogExportView.as_view(), name='questions_catalog_export'),
    url(r'^catalogs/import/(?P<format>[a-z]+)/$', CatalogImportXMLView.as_view(), name='questions_catalog_import'),
    url(r'^catalogs/', CatalogsView.as_view(), name='catalogs'),
]

# internal AJAX API
internal_router = routers.DefaultRouter()
internal_router.register(r'catalogs', CatalogViewSet, base_name='catalog')
internal_router.register(r'sections', SectionViewSet, base_name='section')
internal_router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
internal_router.register(r'questions', QuestionViewSet, base_name='question')
internal_router.register(r'attributes', AttributeViewSet, base_name='attribute')
internal_router.register(r'widgettypes', WidgetTypeViewSet, base_name='widgettype')
internal_router.register(r'valuetypes', ValueTypeViewSet, base_name='valuetype')
internal_router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
internal_router.register(r'conditions', ConditionViewSet, base_name='condition')
internal_router.register(r'settings', SettingsViewSet, base_name='setting')

questions_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API
api_router = routers.DefaultRouter()
api_router.register(r'catalogs', CatalogApiViewSet, base_name='catalog')
api_router.register(r'sections', SectionApiViewSet, base_name='section')
api_router.register(r'questionsets', QuestionSetApiViewSet, base_name='questionset')
api_router.register(r'questions', QuestionApiViewSet, base_name='question')

questions_patterns_api = [
    url(r'^', include(api_router.urls)),
]
