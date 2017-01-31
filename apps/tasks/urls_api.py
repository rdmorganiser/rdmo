from django.conf.urls import url, include

from rest_framework import routers

from .views import TaskViewSet, AttributeViewSet, ConditionViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='task')
router.register(r'attributes', AttributeViewSet, base_name='attribute')
router.register(r'conditions', ConditionViewSet, base_name='condition')

urlpatterns = [
    url(r'^', include(router.urls)),
]
