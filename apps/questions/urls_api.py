from django.conf.urls import url, include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'catalogs', CatalogViewSet, base_name='catalog')
router.register(r'sections', SectionViewSet, base_name='section')
router.register(r'subsections', SubsectionViewSet, base_name='subsection')
router.register(r'entities', QuestionEntityViewSet, base_name='entity')
router.register(r'questions', QuestionViewSet, base_name='question')
router.register(r'attributeentities', AttributeEntityViewSet, base_name='attributeentity')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'widgettypes', WidgetTypeViewSet, base_name='widgettype')

urlpatterns = [
    url(r'^', include(router.urls)),
]
