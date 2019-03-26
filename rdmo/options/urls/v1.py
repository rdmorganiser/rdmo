from django.urls import include, path

from rest_framework import routers

from ..viewsets import OptionApiViewSet, OptionSetApiViewSet

app_name = 'api-v1-options'

router = routers.DefaultRouter()
router.register(r'optionsets', OptionSetApiViewSet, base_name='optionset')
router.register(r'options', OptionApiViewSet, base_name='option')

urlpatterns = [
    path('', include(router.urls)),
]
