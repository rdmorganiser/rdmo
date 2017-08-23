from django.conf.urls import url, include

from rest_framework import routers

from .views import CatalogsView, CatalogExportView
from .viewsets import (
    CatalogViewSet,
    SectionViewSet,
    SubsectionViewSet,
    QuestionSetViewSet,
    QuestionViewSet,
    AttributeEntityViewSet,
    AttributeViewSet,
    WidgetTypeViewSet,
    CatalogApiViewSet,
    SectionApiViewSet,
    SubsectionApiViewSet,
    QuestionSetApiViewSet,
    QuestionApiViewSet,
)


# regular views

questions_patterns = [
    url(r'^catalogs/(?P<pk>[0-9]+)/export/(?P<format>[a-z]+)/$', CatalogExportView.as_view(), name='questions_catalog_export'),
    url(r'^catalogs/', CatalogsView.as_view(), name='catalogs'),
]

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'catalogs', CatalogViewSet, base_name='catalog')
internal_router.register(r'sections', SectionViewSet, base_name='section')
internal_router.register(r'subsections', SubsectionViewSet, base_name='subsection')
internal_router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
internal_router.register(r'questions', QuestionViewSet, base_name='question')
internal_router.register(r'entities', AttributeEntityViewSet, base_name='entity')
internal_router.register(r'attributes', AttributeViewSet, base_name='attribute')
internal_router.register(r'widgettypes', WidgetTypeViewSet, base_name='widgettype')

questions_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'catalogs', CatalogApiViewSet, base_name='catalog')
api_router.register(r'sections', SectionApiViewSet, base_name='section')
api_router.register(r'subsections', SubsectionApiViewSet, base_name='subsection')
api_router.register(r'questionsets', QuestionSetApiViewSet, base_name='questionset')
api_router.register(r'questions', QuestionApiViewSet, base_name='question')

questions_patterns_api = [
    url(r'^', include(api_router.urls)),
]
