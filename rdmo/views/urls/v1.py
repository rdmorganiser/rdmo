from django.urls import include, path

from rest_framework import routers

from ..viewsets import ViewApiViewSet

app_name = 'api-v1-views'

router = routers.DefaultRouter()
router.register(r'views', ViewApiViewSet, base_name='view')

urlpatterns = [
    path('', include(router.urls)),
]
