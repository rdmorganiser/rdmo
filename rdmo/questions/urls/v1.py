from django.urls import include, path

from rest_framework import routers

from ..viewsets import (
    CatalogApiViewSet,
    SectionApiViewSet,
    QuestionSetApiViewSet,
    QuestionApiViewSet
)

app_name = 'api-v1-questions'

router = routers.DefaultRouter()
router.register(r'catalogs', CatalogApiViewSet, base_name='catalog')
router.register(r'sections', SectionApiViewSet, base_name='section')
router.register(r'questionsets', QuestionSetApiViewSet, base_name='questionset')
router.register(r'questions', QuestionApiViewSet, base_name='question')

urlpatterns = [
    path('', include(router.urls)),
]
