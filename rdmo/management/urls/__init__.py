from django.urls import path

from ..views import ImportView, UploadView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('import/', ImportView.as_view(), name='import'),
]
