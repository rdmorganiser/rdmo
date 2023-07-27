from django.urls import re_path

from ..views import ManagementView

urlpatterns = [
    re_path('', ManagementView.as_view(), name='management')
]
