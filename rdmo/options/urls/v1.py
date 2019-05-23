from django.urls import include, path

from rest_framework import routers

from ..viewsets import OptionSetViewSet, OptionViewSet

app_name = 'v1-options'

router = routers.DefaultRouter()
router.register(r'optionsets', OptionSetViewSet, basename='optionset')
router.register(r'options', OptionViewSet, basename='option')

urlpatterns = [
    path('', include(router.urls)),
]
