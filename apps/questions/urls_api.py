from django.conf.urls import url, include

from rest_framework import routers

from .views import (
    CatalogViewSet,
    SectionViewSet,
    SubsectionViewSet,
    QuestionSetViewSet,
    QuestionViewSet,
    AttributeEntityViewSet,
    AttributeViewSet,
    WidgetTypeViewSet
)


router = routers.DefaultRouter()
router.register(r'catalogs', CatalogViewSet, base_name='catalog')
router.register(r'sections', SectionViewSet, base_name='section')
router.register(r'subsections', SubsectionViewSet, base_name='subsection')
router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
router.register(r'questions', QuestionViewSet, base_name='question')
router.register(r'entities', AttributeEntityViewSet, base_name='entity')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'widgettypes', WidgetTypeViewSet, base_name='widgettype')

urlpatterns = [
    url(r'^', include(router.urls)),
]
