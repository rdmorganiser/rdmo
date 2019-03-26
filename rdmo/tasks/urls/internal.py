from django.urls import include, path

from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from ..viewsets import TaskViewSet, AttributeViewSet, ConditionViewSet

app_name = 'internal-tasks'

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='task')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'conditions', ConditionViewSet, base_name='condition')
router.register(r'settings', SettingsViewSet, base_name='setting')

urlpatterns = [
    path('', include(router.urls)),
]
