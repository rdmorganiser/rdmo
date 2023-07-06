from django.urls import path

from ..views import ManagementView

urlpatterns = [
    path('', ManagementView.as_view(), name='management')
]
