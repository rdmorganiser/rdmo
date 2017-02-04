from django.conf.urls import url, include

from rest_framework import routers

from .views import ProjectViewSet, ValueViewSet, QuestionEntityViewSet, CatalogViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='project')
router.register(r'values', ValueViewSet, base_name='value')
router.register(r'entities', QuestionEntityViewSet, base_name='entity')
router.register(r'catalogs', CatalogViewSet, base_name='catalog')

urlpatterns = [
    url(r'^', include(router.urls)),
]
