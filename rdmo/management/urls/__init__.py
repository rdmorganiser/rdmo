from django.urls import path
from django.views.generic.base import RedirectView

from ..views import ImportView, UploadView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='catalogs'), name='management'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('import/', ImportView.as_view(), name='import')
]
