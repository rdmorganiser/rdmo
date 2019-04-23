from django.urls import include, path

from rest_framework import routers

from ..viewsets import (
    ProjectViewSet,
    ValueViewSet,
    QuestionSetViewSet,
    CatalogViewSet
)

app_name = 'internal-projects'

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='project')
router.register(r'values', ValueViewSet, base_name='value')
router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
router.register(r'catalogs', CatalogViewSet, base_name='catalog')

urlpatterns = [
    path('', include(router.urls)),
]
