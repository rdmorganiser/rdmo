from django.urls import include, path

from rest_framework import routers

from ..viewsets import OptionSetViewSet, OptionViewSet

app_name = 'v1-options'

router = routers.DefaultRouter()
try:
    router.register(r'optionsets', OptionSetViewSet, basename='optionset')
    router.register(r'options', OptionViewSet, basename='option')
except TypeError:
        router.register(r'optionsets', OptionSetViewSet, base_name='optionset')
        router.register(r'options', OptionViewSet, base_name='option')

urlpatterns = [
    path('', include(router.urls)),
]
