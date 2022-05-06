from django.urls import path

from ..views import ManagementView, ImportView, UploadView

urlpatterns = [
    path('', ManagementView.as_view(), name='management'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('import/', ImportView.as_view(), name='import')
]
