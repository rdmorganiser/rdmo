from django.urls import path, re_path

from ..views import ManagementView, ImportView, UploadView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('import/', ImportView.as_view(), name='import'),
    re_path('', ManagementView.as_view(), name='management')
]
