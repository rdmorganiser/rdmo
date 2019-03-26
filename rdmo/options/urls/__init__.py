from django.urls import include, re_path

from rest_framework import routers

from ..views import OptionsExportView, OptionsImportXMLView, OptionsView

urlpatterns = [
    re_path(r'^$', OptionsView.as_view(), name='options'),
    re_path(r'^export/(?P<format>[a-z]+)/$', OptionsExportView.as_view(), name='options_export'),
    re_path(r'^import/(?P<format>[a-z]+)/$', OptionsImportXMLView.as_view(), name='options_import'),
]
