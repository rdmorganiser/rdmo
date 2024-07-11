from django.contrib import admin
from django.urls import include, path, re_path

from rdmo.core.views import about, home

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),

    path('', include('rdmo.core.urls')),
    # re_path(r'^api/(?P<version>(v1))/', include('rdmo.core.urls.v1')),
    path('api/v1/', include('rdmo.core.urls.v1')),
    re_path(r'^api/(?P<version>(v1))/', include('rdmo.core.urls.openapi')),
    # path('api/v1/', include('rdmo.core.urls.openapi', namespace='v1')),

    path('admin/', admin.site.urls),
]
