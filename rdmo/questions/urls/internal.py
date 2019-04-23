from django.urls import include, path

from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from ..viewsets import (AttributeViewSet, CatalogViewSet, ConditionViewSet,
                        OptionSetViewSet, QuestionSetViewSet, QuestionViewSet,
                        SectionViewSet, ValueTypeViewSet, WidgetTypeViewSet)

app_name = 'internal-questions'

router = routers.DefaultRouter()
router.register(r'catalogs', CatalogViewSet, base_name='catalog')
router.register(r'sections', SectionViewSet, base_name='section')
router.register(r'questionsets', QuestionSetViewSet, base_name='questionset')
router.register(r'questions', QuestionViewSet, base_name='question')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'widgettypes', WidgetTypeViewSet, base_name='widgettype')
router.register(r'valuetypes', ValueTypeViewSet, base_name='valuetype')
router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
router.register(r'conditions', ConditionViewSet, base_name='condition')
router.register(r'settings', SettingsViewSet, base_name='setting')

urlpatterns = [
    path('', include(router.urls)),
]
