from django.contrib import admin
from django.urls import include, path

from rdmo.core.views import about, home

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),

    path('', include('rdmo.core.urls')),
    path('api/v1/', include('rdmo.core.urls.v1')),
    path('api/v1/', include('rdmo.core.urls.swagger')),

    path('admin/', admin.site.urls),
]
