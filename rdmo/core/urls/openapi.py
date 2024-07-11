from django.contrib.auth.decorators import login_required
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# TODO: maybe generate the schema.yml as part of the build process?

urlpatterns = [
    # http://127.0.0.1:8000/api/v1/
    path('', login_required(SpectacularAPIView.as_view()), name='schema'),
    # http://127.0.0.1:8000/api/v1/swagger/
    path('swagger/', login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    # http://127.0.0.1:8000/api/v1/redoc/
    path('redoc/', login_required(SpectacularRedocView.as_view(url_name='schema')), name='redoc-ui')
]
