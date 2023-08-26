from django.urls import include, path

from rest_framework import routers

from ..viewsets import UserViewSet

app_name = 'v1-accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
