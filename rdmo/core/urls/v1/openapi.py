from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import RedirectView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = 'v1-openapi'

urlpatterns = [
    path('schema/', login_required(SpectacularAPIView.as_view()), name='schema'),
    path('swagger/', login_required(SpectacularSwaggerView.as_view(url_name='v1-openapi:schema')), name='swagger'),
    path('redoc/', login_required(SpectacularRedocView.as_view(url_name='v1-openapi:schema')), name='redoc'),
    path('', RedirectView.as_view(pattern_name='api', permanent=False))
]
