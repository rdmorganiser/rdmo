from django.urls import path

from ..views import reset_overlays

urlpatterns = [
    path('reset/', reset_overlays, name='reset_overlays')
]
