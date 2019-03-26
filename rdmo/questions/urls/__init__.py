from django.urls import include, re_path

from rest_framework import routers

from ..views import CatalogExportView, CatalogImportXMLView, CatalogsView

urlpatterns = [
    re_path(r'^catalogs/(?P<pk>[0-9]+)/export/(?P<format>[a-z]+)/$', CatalogExportView.as_view(), name='questions_catalog_export'),
    re_path(r'^catalogs/import/(?P<format>[a-z]+)/$', CatalogImportXMLView.as_view(), name='questions_catalog_import'),
    re_path(r'^catalogs/', CatalogsView.as_view(), name='catalogs'),
]
