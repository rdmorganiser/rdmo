from django.urls import include, re_path

from rest_framework import routers

from rdmo.core.views import SettingsViewSet

from ..views import ConditionsView, ConditionsExportView, ConditionsImportXMLView

urlpatterns = [
    re_path(r'^$', ConditionsView.as_view(), name='conditions'),
    re_path(r'^export/(?P<format>[a-z]+)/$', ConditionsExportView.as_view(), name='conditions_export'),
    re_path(r'^import/(?P<format>[a-z]+)/$', ConditionsImportXMLView.as_view(), name='conditions_import'),
]
