from django.contrib import admin
from django.urls import include, path

from rdmo.core.views import about, api, home

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('api/', api, name='api'),

    path('', include('rdmo.core.urls')),
    path('api/v1/', include('rdmo.core.urls.v1')),
    path('api/v1/', include('rdmo.core.urls.v1.openapi', namespace='v1')),

    path('admin/', admin.site.urls),
]
