from django.urls import include, path

from rest_framework import routers

from ..viewsets import (
    CatalogViewSet,
    SectionViewSet,
    QuestionSetViewSet,
    QuestionViewSet,
    ValueTypeViewSet,
    WidgetTypeViewSet
)

app_name = 'v1-questions'

router = routers.DefaultRouter()
router.register(r'catalogs', CatalogViewSet, base_name='catalog')
router.register(r'sections', SectionViewSet, base_name='section')
router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
router.register(r'questions', QuestionViewSet, base_name='question')
router.register(r'widgettypes', WidgetTypeViewSet, base_name='widgettype')
router.register(r'valuetypes', ValueTypeViewSet, base_name='valuetype')

urlpatterns = [
    path('', include(router.urls)),
]
