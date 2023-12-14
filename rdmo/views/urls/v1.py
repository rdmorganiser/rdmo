from django.urls import include, path

from rest_framework import routers

from ..viewsets import ViewToggleCurrentSiteViewSet, ViewViewSet

app_name = 'v1-views'

router = routers.DefaultRouter()
router.register(r'views', ViewViewSet, basename='view')
router.register(r'view-toggle-site', ViewToggleCurrentSiteViewSet, basename='view-toggle-site')

urlpatterns = [
    path('', include(router.urls)),
]
