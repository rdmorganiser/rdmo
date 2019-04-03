from django.urls import include, path

from rest_framework import routers

from ..viewsets import ViewViewSet

app_name = 'v1-views'

router = routers.DefaultRouter()
router.register(r'views', ViewViewSet, base_name='view')

urlpatterns = [
    path('', include(router.urls)),
]
