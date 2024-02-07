from django.urls import include, path

from rest_framework import routers

from ..viewsets import (
    CatalogViewSet,
    PageViewSet,
    QuestionSetViewSet,
    QuestionViewSet,
    SectionViewSet,
    ValueTypeViewSet,
    WidgetTypeViewSet,
)

app_name = 'v1-questions'

router = routers.DefaultRouter()
router.register(r'catalogs', CatalogViewSet, basename='catalog')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'pages', PageViewSet, basename='page')
router.register(r'questionsets', QuestionSetViewSet, basename='questionset')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'widgettypes', WidgetTypeViewSet, basename='widgettype')
router.register(r'valuetypes', ValueTypeViewSet, basename='valuetype')

urlpatterns = [
    path('', include(router.urls)),
]
