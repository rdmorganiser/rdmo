from django.urls import include, re_path

from rest_framework import routers

from ..views import DomainExportView, DomainImportXMLView, DomainView


urlpatterns = [
    re_path(r'^$', DomainView.as_view(), name='domain'),
    re_path(r'^export/(?P<format>[a-z]+)/$', DomainExportView.as_view(), name='domain_export'),
    re_path(r'^import/(?P<format>[a-z]+)/$', DomainImportXMLView.as_view(), name='domain_import'),
]
