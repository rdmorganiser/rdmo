from django.conf.urls import url, include

from rest_framework import routers

from .views import ViewViewSet

router = routers.DefaultRouter()
router.register(r'views', ViewViewSet, base_name='view')

urlpatterns = [
    url(r'^', include(router.urls)),
]
