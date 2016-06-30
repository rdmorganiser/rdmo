from django.conf.urls import url, include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='project')
router.register(r'values', ValueViewSet, base_name='value')

urlpatterns = [
    url(r'^', include(router.urls)),
]
