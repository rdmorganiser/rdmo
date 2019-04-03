from django.urls import include, path

from rest_framework import routers

from ..viewsets import UserViewSet


app_name = 'api-v1-accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = [
    path('', include(router.urls)),
]
